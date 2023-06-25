from rest_framework import serializers
from custom_auth.models import MainUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()
