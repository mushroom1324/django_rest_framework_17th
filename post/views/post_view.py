from post.models import Post
from post.models.serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here, using CBV
class PostList(APIView):

        @staticmethod
        def get(request):
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

        @staticmethod
        def post(request):

            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)

            return Response(serializer.errors, status=400)
        