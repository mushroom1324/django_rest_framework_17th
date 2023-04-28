from rest_framework import serializers
from post.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'parent', 'user', 'post', 'content', 'likes', 'created_at', 'updated_at')
