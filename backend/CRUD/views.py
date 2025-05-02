from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Transaction, Category, Budget, Notification
from .serializers import TransactionSerializer, CategorySerializer, BudgetSerializer, NotificationSerializer
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class AddTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(user=request.user)
            
            # After saving transaction, check if it triggers any budget alerts
            check_budget_alerts(request.user, transaction)
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class RetrieveTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date_created')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    

class RetrieveTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id, user=request.user)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=404)
        

class UpdateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id, user=request.user)
            serializer = TransactionSerializer(transaction, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=404)
        
class DeleteTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id, user=request.user)
            transaction.delete()
            return Response({"message": "Transaction deleted successfully."}, status=204)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=404)
        

class AddCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class RetrieveCategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date_created')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
class FilterTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        category = request.query_params.get('category')
        transaction_type = request.query_params.get('type')

        transactions = Transaction.objects.filter(user=request.user)
        if start_date and end_date:
            transactions = transactions.filter(date_created__range=[start_date, end_date])
        if category:
            transactions = transactions.filter(category__id=category)
        if transaction_type:
            transactions = transactions.filter(type=transaction_type)

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    

class FinancialSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_income = Transaction.objects.filter(user=request.user, type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = Transaction.objects.filter(user=request.user, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        category_summary = Transaction.objects.filter(user=request.user).values('category__name').annotate(total=Sum('amount'))
        return Response({
            "total_income": total_income,
            "total_expenses": total_expenses,
            "category_summary": category_summary
        })
    

class SetBudgetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the user already has a budget
            budget, created = Budget.objects.update_or_create(
                user=request.user,
                defaults={'monthly_budget': serializer.validated_data['monthly_budget']}
            )
            return Response(BudgetSerializer(budget).data, status=201)
        return Response(serializer.errors, status=400)
    

class RetrieveBudgetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            budget = Budget.objects.get(user=request.user)
            serializer = BudgetSerializer(budget)
            return Response(serializer.data)
        except Budget.DoesNotExist:
            return Response({"error": "Budget not set."}, status=404)
        

class UpdateBudgetView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            budget = Budget.objects.get(user=request.user)
            serializer = BudgetSerializer(budget, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Budget.DoesNotExist:
            return Response({"error": "Budget not set."}, status=404)
        
class BudgetAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            budget = Budget.objects.get(user=request.user)
            total_expenses = Transaction.objects.filter(user=request.user, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
            remaining_budget = budget.monthly_budget - total_expenses

            return Response({
                "monthly_budget": budget.monthly_budget,
                "total_expenses": total_expenses,
                "remaining_budget": remaining_budget,
                "status": "Under Budget" if remaining_budget >= 0 else "Over Budget"
            })
        except Budget.DoesNotExist:
            return Response({"error": "Budget not set."}, status=404)

def get_weekly_financial_overview(user):
    """
    Service function to retrieve weekly financial data for a user.
    Returns total income, expenses, net balance and category breakdown for the past week.
    """
    # Calculate the date range for the past week
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    
    # Get transactions for the past week
    weekly_transactions = Transaction.objects.filter(
        user=user,
        date_created__range=[start_date, end_date]
    )
    
    # Calculate total income
    weekly_income = weekly_transactions.filter(
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate total expenses
    weekly_expenses = weekly_transactions.filter(
        type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Calculate net balance
    net_balance = weekly_income - weekly_expenses
    
    # Get category breakdown
    category_breakdown = weekly_transactions.values(
        'category__name', 'type'
    ).annotate(total=Sum('amount'))
    
    # Format category breakdown into a more usable structure
    formatted_breakdown = {}
    for item in category_breakdown:
        category_name = item['category__name']
        if category_name not in formatted_breakdown:
            formatted_breakdown[category_name] = {
                'income': 0,
                'expense': 0,
                'net': 0
            }
        
        formatted_breakdown[category_name][item['type']] = item['total']
        formatted_breakdown[category_name]['net'] = (
            formatted_breakdown[category_name]['income'] - 
            formatted_breakdown[category_name]['expense']
        )
    
    return {
        'start_date': start_date,
        'end_date': end_date,
        'weekly_income': weekly_income,
        'weekly_expenses': weekly_expenses,
        'net_balance': net_balance,
        'category_breakdown': formatted_breakdown
    }

class WeeklyFinancialOverviewView(APIView):
    """
    API endpoint that returns a weekly overview of the user's finances.
    Includes total income, expenses, net balance and category breakdown for the past 7 days.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Use the service function to get weekly financial data
        weekly_overview = get_weekly_financial_overview(request.user)
        
        return Response(weekly_overview)

# Notification Center APIs

class NotificationCenterView(APIView):
    """
    API endpoint to fetch all notifications for a user.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class MarkNotificationReadView(APIView):
    """
    API endpoint to mark notifications as read.
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            notification = Notification.objects.get(id=id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({'status': 'success'})
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)

class MarkAllNotificationsReadView(APIView):
    """
    API endpoint to mark all notifications as read.
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'success'})

class UnreadNotificationsCountView(APIView):
    """
    API endpoint to get the count of unread notifications.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})

# Budget Alerts and Notification Services

def check_budget_alerts(user, transaction=None):
    """
    Check if the user has exceeded their budget and create a notification if they have.
    This can be called after any new expense transaction.
    """
    try:
        budget = Budget.objects.get(user=user)
        total_expenses = Transaction.objects.filter(
            user=user, 
            type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        remaining_budget = budget.monthly_budget - total_expenses
        
        # If budget is exceeded
        if remaining_budget < 0:
            # Create notification
            notification = Notification.objects.create(
                user=user,
                type='budget_exceeded',
                title='Budget Alert',
                message=f'You have exceeded your monthly budget of {budget.monthly_budget}. Current expenses: {total_expenses}.'
            )
            
            # Send real-time notification
            send_real_time_notification(user.id, {
                'type': 'budget_exceeded',
                'title': 'Budget Alert',
                'message': f'You have exceeded your monthly budget of {budget.monthly_budget}.',
                'id': notification.id
            })
            
            return True
        
        # If getting close to budget (90%)
        elif remaining_budget <= (budget.monthly_budget * 0.1):
            # Create notification
            notification = Notification.objects.create(
                user=user,
                type='low_balance',
                title='Budget Warning',
                message=f'You are close to your monthly budget of {budget.monthly_budget}. Remaining: {remaining_budget}.'
            )
            
            # Send real-time notification
            send_real_time_notification(user.id, {
                'type': 'low_balance',
                'title': 'Budget Warning',
                'message': f'You are close to your monthly budget. Remaining: {remaining_budget}.',
                'id': notification.id
            })
            
            return True
    
    except Budget.DoesNotExist:
        # No budget set
        pass
    
    return False

def send_real_time_notification(user_id, notification_data):
    """
    Send a real-time notification to the client using WebSockets.
    """
    channel_layer = get_channel_layer()
    
    # Send to the user's notification channel
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user_id}',
        {
            'type': 'send_notification',
            'notification': notification_data
        }
    )

@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    """
    Signal handler that runs after a transaction is saved.
    Used to check budget status and trigger notifications if needed.
    """
    if created and instance.type == 'expense':
        check_budget_alerts(instance.user, instance)
        
        # If it's a large expense (over 20% of budget), create a notification
        try:
            budget = Budget.objects.get(user=instance.user)
            if instance.amount > (budget.monthly_budget * 0.2):
                notification = Notification.objects.create(
                    user=instance.user,
                    type='large_expense',
                    title='Large Expense Alert',
                    message=f'You just made a large expense of {instance.amount} ({int(instance.amount/budget.monthly_budget*100)}% of your monthly budget).'
                )
                
                send_real_time_notification(instance.user.id, {
                    'type': 'large_expense',
                    'title': 'Large Expense Alert',
                    'message': f'You just made a large expense of {instance.amount}.',
                    'id': notification.id
                })
        except Budget.DoesNotExist:
            pass