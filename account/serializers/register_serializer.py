from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return user
