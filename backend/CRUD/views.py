from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer
from .serializers import TransactionSerializer
from django.db.models import Sum
from .models import Budget
from .serializers import BudgetSerializer

"""
CRUD API views for managing transactions, categories, and budgets.
Includes endpoints for creating, retrieving, updating, and deleting transactions and categories, as well as setting and retrieving budgets."""



"""
        Add a new transaction.
        Expects a POST request with transaction data in the request body.
        Validates the data and saves the transaction to the database.
        Returns the created transaction data or an error message if validation fails.
 """
class AddTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    



"""     Retrieve all transactions for the authenticated user.
        Expects a GET request.
        Returns a list of transactions in the response body.
        If no transactions are found, returns an empty list.

"""
class RetrieveTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date_created')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    





"""
        Retrieve a specific transaction by ID.
        Expects a GET request with the transaction ID in the URL.   
        Returns the transaction data in the response body.
        If the transaction is not found, returns an error message.
        
"""
class RetrieveTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id, user=request.user)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=404)
        

        

"""
        Update a specific transaction by ID.
        Expects a PUT request with the transaction ID in the URL and updated data in the request body.
        Validates the data and updates the transaction in the database.
        Returns the updated transaction data or an error message if validation fails.
        If the transaction is not found, returns an error message.
        
"""
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



"""     Delete a specific transaction by ID.
        Expects a DELETE request with the transaction ID in the URL.
        Deletes the transaction from the database.
        Returns a success message or an error message if the transaction is not found.
        If the transaction is not found, returns an error message.
        
"""
class DeleteTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id, user=request.user)
            transaction.delete()
            return Response({"message": "Transaction deleted successfully."}, status=204)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=404)
        

        
"""
        Add a new category.
        Expects a POST request with category data in the request body.
        Validates the data and saves the category to the database.
        Returns the created category data or an error message if validation fails.
        If the category is not found, returns an error message.

"""
class AddCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    


    
"""     Retrieve all categories.
        Expects a GET request.
        Returns a list of categories in the response body.
        If no categories are found, returns an empty list.

        If the category is not found, returns an error message.


"""
class RetrieveCategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    

    
"""
        Retrieve a specific category by ID.
        Expects a GET request with the category ID in the URL.
        Returns the category data in the response body.
        If the category is not found, returns an error message.

"""
class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date_created')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    




"""     Filter transactions based on date range, category, and type.
        Expects a GET request with query parameters for start_date, end_date, category, and type.
        Filters the transactions based on the provided parameters and returns the filtered transactions.
        If no transactions match the criteria, returns an empty list.
        If the category is not found, returns an error message.
        If the transaction type is not found, returns an error message.
"""   
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
    


    

"""
        Retrieve a financial summary for the authenticated user.
        Expects a GET request.
        Returns the total income, total expenses, and category-wise summary of transactions.
        If no transactions are found, returns zero for total income and expenses.
        If the category is not found, returns an error message.
        If the transaction type is not found, returns an error message.
        
"""
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

    
    

"""
        Retrieve the budget for the authenticated user.
        Expects a GET request.
        Returns the budget data in the response body.
        If the budget is not set, returns an error message.
        If the budget is not found, returns an error message.
        If the user is not authenticated, returns an error message.
"""
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
    




"""
        Retrieve the budget for the authenticated user.
        Expects a GET request.
        Returns the budget data in the response body.
        If the budget is not set, returns an error message.

        If the budget is not found, returns an error message.
        If the user is not authenticated, returns an error message.
        If the budget is not set, returns an error message."""
class RetrieveBudgetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            budget = Budget.objects.get(user=request.user)
            serializer = BudgetSerializer(budget)
            return Response(serializer.data)
        except Budget.DoesNotExist:
            return Response({"error": "Budget not set."}, status=404)
        


        
"""Update the budget for the authenticated user.
        Expects a PUT request with updated budget data in the request body.
        Validates the data and updates the budget in the database.
        Returns the updated budget data or an error message if validation fails.
        If the budget is not found, returns an error message.
        If the user is not authenticated, returns an error message.
        If the budget is not set, returns an error message.
        If the budget is not found, returns an error message."""
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
    

        

"""_summary_of_budget_analysis(self):
        Retrieve a summary of the budget analysis for the authenticated user.
        Expects a GET request.
        Returns the monthly budget, total expenses, remaining budget, and status (under or over budget).
        If the budget is not set, returns an error message.
        If the budget is not found, returns an error message
"""
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
        
