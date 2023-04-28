from rest_framework import serializers
from subject.models.subject import Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'subject_name', 'professor_name', 'contact', 'location_info', 'time', 'is_cyber')
