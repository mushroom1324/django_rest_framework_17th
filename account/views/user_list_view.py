from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from account.serializers import UserSerializer


class UserListAPIView(APIView):

    @staticmethod
    def get(request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
