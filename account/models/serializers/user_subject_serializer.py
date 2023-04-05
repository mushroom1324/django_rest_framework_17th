from rest_framework import serializers
from account.models.user_subject import UserSubject


class UserSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubject
        fields = ('id', 'user', 'subject')
