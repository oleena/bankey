from rest_framework import serializers
from core.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

    class Meta:
        model = CustomUser
        fields = ("username", "password", "balance")
