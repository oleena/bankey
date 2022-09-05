from django.urls import path

from core.views import SignUpView, DashboardView, BalanceView, TransferView

urlpatterns = [
    path("", BalanceView.as_view(), name="balance"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("balance/", BalanceView.as_view(), name="balance"),
    path("transfer/", TransferView.as_view(), name="transfer"),
]
