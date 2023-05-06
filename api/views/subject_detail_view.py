from rest_framework.views import APIView
from rest_framework.response import Response
from subject.models import Subject
from subject.serializers import SubjectSerializer


class SubjectDetailViewSet(APIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @staticmethod
    def get(request, pk):
        subject = Subject.objects.get(pk=pk)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        subject = Subject.objects.get(pk=pk)
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @staticmethod
    def patch(request, pk):
        subject = Subject.objects.get(pk=pk)
        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @staticmethod
    def delete(request, pk):
        subject = Subject.objects.get(pk=pk)
        subject.delete()
        return Response(status=204)
