from .subject_view import SubjectViewSet


subject_list = SubjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
