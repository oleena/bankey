from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import CustomUserCreationForm
from core.models import CustomUser


class CustomUserAdmin(UserAdmin):
    form = CustomUserCreationForm
    model = CustomUser
    list_display = ["username", "balance"]


admin.site.register(CustomUser, CustomUserAdmin)
