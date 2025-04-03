from django.urls import path
from .views import (
    AddTransactionView,
    RetrieveTransactionsView,
    RetrieveTransactionView,
    UpdateTransactionView,
    DeleteTransactionView,
    AddCategoryView,
    RetrieveCategoriesView,
    TransactionHistoryView,
    FilterTransactionsView,
    FinancialSummaryView,
    SetBudgetView,
    RetrieveBudgetView,
    UpdateBudgetView,
    BudgetAnalysisView,
    
)

urlpatterns = [
    path('transactions/', AddTransactionView.as_view(), name='add-transaction'),
    path('transactions/all/', RetrieveTransactionsView.as_view(), name='retrieve-transactions'),
    path('transactions/<int:id>/', RetrieveTransactionView.as_view(), name='retrieve-transaction'),
    path('transactions/<int:id>/update/', UpdateTransactionView.as_view(), name='update-transaction'),
    path('transactions/<int:id>/delete/', DeleteTransactionView.as_view(), name='delete-transaction'),
    path('categories/', AddCategoryView.as_view(), name='add-category'),
    path('categories/all/', RetrieveCategoriesView.as_view(), name='retrieve-categories'),
    path('dashboard/history/', TransactionHistoryView.as_view(), name='transaction-history'),
    path('dashboard/filter/', FilterTransactionsView.as_view(), name='filter-transactions'),
    path('dashboard/summary/', FinancialSummaryView.as_view(), name='financial-summary'),
    path('budget/', SetBudgetView.as_view(), name='set-budget'),
    path('budget/retrieve/', RetrieveBudgetView.as_view(), name='retrieve-budget'),
    path('budget/update/', UpdateBudgetView.as_view(), name='update-budget'),
    path('budget/analysis/', BudgetAnalysisView.as_view(), name='budget-analysis'),
]