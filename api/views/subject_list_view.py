from rest_framework.response import Response
from subject.models import Subject
from subject.serializers import SubjectSerializer
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .subject_filter_view import SubjectFilter
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class SubjectListViewSet(APIView):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter

    @staticmethod
    @permission_classes([IsAuthenticated])
    @authentication_classes([JSONWebTokenAuthentication])
    def get(request):
        # get objects which are not deleted
        subjects = Subject.objects.filter(deleted_at__isnull=True)
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
