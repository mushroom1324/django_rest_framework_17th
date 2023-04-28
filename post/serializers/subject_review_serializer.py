from rest_framework import serializers
from subject.models.subject_review import SubjectReview


class SubjectReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectReview
        fields = ('id', 'subject', 'content', 'rate', 'created_at', 'updated_at')
