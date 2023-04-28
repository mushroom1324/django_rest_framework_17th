from rest_framework.response import Response
from subject.models import Subject
from post.serializers import SubjectSerializer
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .subject_filter_view import SubjectFilter


class SubjectListViewSet(APIView):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter

    @staticmethod
    def get(request):
        subjects = Subject.objects.all()
        filtered_subjects = SubjectFilter(request.GET, queryset=subjects)
        serializer = SubjectSerializer(filtered_subjects.qs, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):

        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    @staticmethod
    def put(request, pk):
        subject = Subject.objects.get(pk=pk)
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @staticmethod
    def delete(request, pk):
        subject = Subject.objects.get(pk=pk)
        subject.delete()
        return Response(status=204)
