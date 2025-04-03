from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer
from .serializers import TransactionSerializer
from django.db.models import Sum
from .models import Budget
from .serializers import BudgetSerializer

class AddTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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