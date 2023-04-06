from rest_framework.viewsets import ModelViewSet
from subject.models import Subject
from subject.models.serializers import SubjectSerializer


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


subject_list = SubjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
