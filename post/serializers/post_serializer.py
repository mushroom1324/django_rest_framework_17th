from rest_framework import serializers
from post.models.post import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'subject', 'category', 'title', 'content', 'likes', 'created_at', 'updated_at')
