from decimal import Decimal

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from core.models import CustomUser
from core.forms import CustomUserCreationForm
from core.serializers import UserSerializer


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    serializer_class = UserSerializer


class BalanceView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "balance.html"

    def get(self, request):
        user = CustomUser.objects.get(username=request.user.username)
        return Response({"balance": user.balance})


class TransferView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        users = CustomUser.objects.exclude(username=request.user.username)
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data},     template_name = "transfer.html")

    def post(self, request):
        try:
            transaction_amount = request.POST['amount']
            sender = CustomUser.objects.get(username=request.user.username)
            if Decimal(transaction_amount) > sender.balance:
                return Response(
                    {
                        "balance": sender.balance,
                        "status": "ERROR",
                        "message": "Insufficient funds.",
                    },
                    template_name="balance.html",
                )
            recipient = request.POST["recipient"]
            receiver = CustomUser.objects.get(username=recipient)
            sender.balance = sender.balance - Decimal(transaction_amount)
            receiver.balance = receiver.balance + Decimal(transaction_amount)
            sender.save()
            receiver.save()
            message = "Transaction Success."
        except Exception as exc:
            message = "Transaction Failure, try again!"
            user = CustomUser.objects.get(username=request.user.username)
            return Response(
                {"balance": user.balance, "status": "ERROR", "message": exc},
                template_name="balance.html",
            )

        user = CustomUser.objects.get(username=request.user.username)
        return Response(
            {"balance": user.balance, "status": "OK", "message": message},
            template_name="balance.html",
        )


class DashboardView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "dashboard.html"

    def get(self, request):
        return Response()
