from django.urls import path
from drf_yasg.utils import swagger_auto_schema
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
    WeeklyFinancialOverviewView,
    NotificationCenterView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView,
    UnreadNotificationsCountView,
)

# Apply swagger_auto_schema to views
AddTransactionView = swagger_auto_schema(
    operation_description="Add a new transaction",
    operation_summary="Create transaction"
)(AddTransactionView)

RetrieveTransactionsView = swagger_auto_schema(
    operation_description="Get all transactions for the authenticated user",
    operation_summary="List all transactions"
)(RetrieveTransactionsView)

RetrieveTransactionView = swagger_auto_schema(
    operation_description="Get a specific transaction by ID",
    operation_summary="Get transaction details"
)(RetrieveTransactionView)

UpdateTransactionView = swagger_auto_schema(
    operation_description="Update a specific transaction by ID",
    operation_summary="Update transaction"
)(UpdateTransactionView)

DeleteTransactionView = swagger_auto_schema(
    operation_description="Delete a specific transaction by ID",
    operation_summary="Delete transaction"
)(DeleteTransactionView)

AddCategoryView = swagger_auto_schema(
    operation_description="Add a new category",
    operation_summary="Create category"
)(AddCategoryView)

RetrieveCategoriesView = swagger_auto_schema(
    operation_description="Get all categories",
    operation_summary="List all categories"
)(RetrieveCategoriesView)

TransactionHistoryView = swagger_auto_schema(
    operation_description="Get transaction history for the authenticated user",
    operation_summary="Get transaction history"
)(TransactionHistoryView)

FilterTransactionsView = swagger_auto_schema(
    operation_description="Filter transactions based on various parameters",
    operation_summary="Filter transactions"
)(FilterTransactionsView)

FinancialSummaryView = swagger_auto_schema(
    operation_description="Get financial summary including income, expenses, and savings",
    operation_summary="Get financial summary"
)(FinancialSummaryView)

SetBudgetView = swagger_auto_schema(
    operation_description="Set or update monthly budget",
    operation_summary="Set budget"
)(SetBudgetView)

RetrieveBudgetView = swagger_auto_schema(
    operation_description="Get the user's monthly budget",
    operation_summary="Get budget"
)(RetrieveBudgetView)

UpdateBudgetView = swagger_auto_schema(
    operation_description="Update the user's monthly budget",
    operation_summary="Update budget"
)(UpdateBudgetView)

BudgetAnalysisView = swagger_auto_schema(
    operation_description="Get budget analysis including spending patterns and recommendations",
    operation_summary="Get budget analysis"
)(BudgetAnalysisView)

WeeklyFinancialOverviewView = swagger_auto_schema(
    operation_description="Get weekly financial overview including income, expenses, and savings",
    operation_summary="Get weekly overview"
)(WeeklyFinancialOverviewView)

NotificationCenterView = swagger_auto_schema(
    operation_description="Get all notifications for the authenticated user",
    operation_summary="List notifications"
)(NotificationCenterView)

MarkNotificationReadView = swagger_auto_schema(
    operation_description="Mark a specific notification as read",
    operation_summary="Mark notification as read"
)(MarkNotificationReadView)

MarkAllNotificationsReadView = swagger_auto_schema(
    operation_description="Mark all notifications as read",
    operation_summary="Mark all notifications as read"
)(MarkAllNotificationsReadView)

UnreadNotificationsCountView = swagger_auto_schema(
    operation_description="Get count of unread notifications",
    operation_summary="Get unread notifications count"
)(UnreadNotificationsCountView)

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
    path('dashboard/weekly-overview/', WeeklyFinancialOverviewView.as_view(), name='weekly-financial-overview'),
    path('budget/', SetBudgetView.as_view(), name='set-budget'),
    path('budget/retrieve/', RetrieveBudgetView.as_view(), name='retrieve-budget'),
    path('budget/update/', UpdateBudgetView.as_view(), name='update-budget'),
    path('budget/analysis/', BudgetAnalysisView.as_view(), name='budget-analysis'),
    
    # Notification routes
    path('notifications/', NotificationCenterView.as_view(), name='notification-center'),
    path('notifications/<int:id>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('notifications/read-all/', MarkAllNotificationsReadView.as_view(), name='mark-all-notifications-read'),
    path('notifications/unread-count/', UnreadNotificationsCountView.as_view(), name='unread-notifications-count'),
]