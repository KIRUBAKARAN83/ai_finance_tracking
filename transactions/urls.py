from django.urls import path

from .views import (
    # User
    dashboard,
    add_transaction,
    edit_transaction,
    delete_transaction,
    all_transactions,

    # Charts / API
    chart_data,

    # Budgets
    create_budget,
    budgets_list,

    # Chatbot
    chat_api,
    chat_stream,

    # Admin
    admin_dashboard,
    admin_users,
    ban_user,
    unban_user,
    delete_user,

    # PWA
    offline,
    delete_budget
    #expense_category_page
    
)
from .views import expense_category_char
from .pdf import monthly_pdf

app_name = "transactions"

urlpatterns = [
    # ================= USER =================
    path("", dashboard, name="dashboard"),
    path("add/", add_transaction, name="add_transaction"),
    path("edit/<int:pk>/", edit_transaction, name="edit_transaction"),
    path("delete/<int:pk>/", delete_transaction, name="delete_transaction"),
    path("transactions/", all_transactions, name="all_transactions"),

    # ================= BUDGETS =================
    path("budgets/", budgets_list, name="budgets_list"),
    path("budgets/add/", create_budget, name="create_budget"),

    # ================= CHAT =================
    path("chat/", chat_api, name="chat"),                # UI / normal chat
    path("chat/stream/", chat_stream, name="chat_stream"),

    # ================= API =================
    path("api/chat/", chat_api, name="chat_api"),        # AJAX chat
    path("api/chart-data/", chart_data, name="chart_data"),

    # ================= PDF =================
    path("pdf/", monthly_pdf, name="monthly_pdf"),

    # ================= ADMIN =================
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-users/", admin_users, name="admin_users"),
    path("admin-users/ban/<int:user_id>/", ban_user, name="ban_user"),
    path("admin-users/unban/<int:user_id>/", unban_user, name="unban_user"),
    path("admin-users/delete/<int:user_id>/", delete_user, name="delete_user"),
    path("charts/expense-category/", expense_category_chart, name="expense_category_chart"),
    #path("expense-page/", expense_category_page, name="expense_category_page"),
    path("budgets/delete/<int:budget_id>/", delete_budget, name="delete_budget"),

    

    # ================= PWA =================
    path("offline/", offline, name="offline"),
]
