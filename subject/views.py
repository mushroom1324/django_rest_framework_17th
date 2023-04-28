from subject.models import Subject
from post.serializers import SubjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here, using CBV
class SubjectList(APIView):

    @staticmethod
    def get(request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):

        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
