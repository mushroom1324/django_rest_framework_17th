from account.models import User
from account.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here, using CBV
class UserList(APIView):

    @staticmethod
    def get(request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
