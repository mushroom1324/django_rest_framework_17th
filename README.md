# CEOS 17기 백엔드 스터디

- 과제의 주제는 [에브리타임](https://everytime.kr/) **데이터 모델링** 해보기!
    - 커뮤니티 기능
    - 시간표(친구맺기 포함)

- api app에 기능들을 구현하였고, 먼저 ERD부터 그려보았다. (처음엔 진짜 그려봤다)

<img width="540" alt="Screen Shot 2023-04-01 at 8 56 08 PM" src="https://user-images.githubusercontent.com/76674422/229287223-29699f98-4855-4bf6-a549-91cbda1126c1.png">

- 그 후 모델 개발하며 적절히 수정하였다.

<img width="1094" alt="Screen Shot 2023-04-01 at 7 47 24 PM" src="https://user-images.githubusercontent.com/76674422/229286962-a08db351-7480-47a0-ad76-63370318142a.png">

- model이 너무 많아 pakage로 분리하여 모델별로 분리하였다.
- **__init__에 임포트 잊지 말자**

### user.py
- OneToOne 방식으로 User모델을 확장하였다.
- 추가적인 기능을 넣기 위해 UserProfile에 저장하였는데, ORM 쿼리로 작업할 때 번거롭다는 단점이 있었다.
- UserProfile 객체를 찾을 때, User모델을 찾고, User모델에 맞는 UserProfile을 찾아야한다. (귀찮다)
- 그렇지만 구현이 간단하다는 장점이 있다.
- 개인적으로 OneToOne방법이 싫진 않다. 만들때 편하다.

- friend_list를 ManyToManyField로 구현해주었다.

<img width="253" alt="Screen Shot 2023-04-01 at 8 52 37 PM" src="https://user-images.githubusercontent.com/76674422/229287061-36d025b1-ac46-4ad7-beb5-cf3dde48dc56.png">


- ManyToMany로 선언하면 장고가 from_userprofile_id, to_userprofile_id로 알아서 풀어준다.
- admin 페이지에 register 후 쉽게 수정 가능하다.

- 다대다 풀어서 쓰는게 좋은거 아닌가요?
- 나도 그렇다고 배웠다. 근데 장고에서 through라는 기능을 제공한다.
```python
class Subject(models.Model):
    # 다른 필드들
    times = models.ManyToManyField(Time, through='Schedule', blank=True)

class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    room = models.CharField(max_length=10)
```
- ManyToManyField의 argument로 through='Schedule'을 받았다.
- 이러면 다대다 연관관계 사이에 Schedule이 생긴다.
- 장고는 파이썬이라 그런지 편의성이 뛰어난 것 같다.

<img width="387" alt="Screen Shot 2023-04-01 at 8 53 30 PM" src="https://user-images.githubusercontent.com/76674422/229287108-c6f9481a-aceb-4004-a048-54d71bb83019.png">

### post.py
(ERD 보세요) 여러 칼럼을 받는다.
``` python
user = models.ForeignKey(User, on_delete=models.CASCADE)

...

created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```
- ForeignKey로 외래 키를 받는다. ('다대일' 중 '다' 관계에 있는 모델에 넣는다.)
- on_delete: ForeignKeyField가 바라보는 값이 삭제될 때 해당 요소를 처리하는 방법을 지정해 준다.
  - CASACADE: ForeignKeyField를 포함하는 모델 인스턴스(row)도 같이 삭제한다.
  - PROTECT : 해당 요소가 같이 삭제되지 않도록 ProtectedError를 발생시킨다.
  - SET_NULL : ForeignKeyField 값을 NULL로 바꾼다.
  - 말고도 더 있다..
- auto_now_add는 객체가 생성될 때 시간을 넣어준다.
- auto_now는 객체가 업데이트 될 때마다 시간을 넣어준다.

### comment.py, reply.py
- 딱히 뭐 없고, __str__을 작성할 때 고민을 했다.
- 댓글에 제목같은건 안달고싶고.. 그렇다고 유저이름 띄우긴 싫고..
- 그래서 달린 게시글 이름이랑 내용 10자만 받기로 했다.

```python
    def __str__(self):
        return str(self.comment.__str__()) + "의 답글: " + str(self.content[:10])
```
reply.py의 __str__인데, 대충 저렇게 해서 이렇게 나온다.

<img width="545" alt="Screen Shot 2023-04-01 at 8 54 19 PM" src="https://user-images.githubusercontent.com/76674422/229287136-904543dc-6f01-4dc5-86e3-59b381756fff.png">

### subject.py
- subject와 user를 ManyToMany로 연결한다.
- 앞서 through 기능을 언급했지만, 이번엔 직접 user_subject를 만들어서 등록해보았다.
>  (One)UserProfile - (Many)UserSubject - (One)Subject

- is_cyber: 싸강이나 아니냐.. 를 받는 boolean. 
- 싸강은 시간이 없으므로 시간이 nullable 해야한다.
- **근데 null=True 하지 말자!!**
- 대신 **blank=True** 하자.
> Django 표준은 빈 값을 빈 문자열로 저장하는 것이며 일관성을 위해서 null값과 빈 값을 빈 문자열을 통해 저장하는 것이다.
- 당최 무슨말일까: null대신 blank=True하면 DB에서는 빈 값이 빈 문자열 ' '으로 설정되서 null과 빈 값을 빈 문자열으로만 판단할 수 있게 된다는 장점을 가질 수 있다.
- 자주 사용되는 CharField / TextField에 대해서는 null=True는 사용하지 말자.
- 그러므로 **blank=True** 하자.

#### 시간을 string으로 받는건 너무 성의 없는거 아닌가요?
- 맞는 말이긴 하다. 그치만 시간 데이터 저장에 관한 내 생각은 이렇다.
- 다른 구현방법: 시간 테이블을 만들고, 강의와 다대다 관계로 묶는다.
- 문제점: 에브리타임은 시간표 커스텀도 가능한데, 이걸 보면 분단위로 시간을 설정할 수 있다.
- 그럼 시간에만 너무 많은 객체가 필요해지고, 강의를 참조할때마다 수많은 시간 객체들 중 맞는걸 검색해서 찾으면 비효율적일 것 같다.
- (정답을 알려주세요)

## shell_commands.md
- 쉘로 모델 관리 해보려고 했는데, 노가다성이 짙다. 너무 귀찮다.
- 그래서 명령어들을 md파일에 적어두고 복사 붙여넣기 하려고 했는데, 우연히 재밌는 기능을 찾았다.
- md파일의 코드블럭 종류를 shell로 해놓고 명령어를 적으니 자동 실행 버튼이 생긴다.

<img width="425" alt="Screen Shot 2023-04-01 at 8 59 44 PM" src="https://user-images.githubusercontent.com/76674422/229287349-227c7baa-e1bf-43bf-8242-b9ef73d43ba8.png">

- 생기죠?

<img width="799" alt="Screen Shot 2023-04-01 at 9 00 14 PM" src="https://user-images.githubusercontent.com/76674422/229287369-c05c84ff-9cfa-4a2f-a6b2-376eac22a0e3.png">

- 실행결과 (filter로 리스트를 받아서 하나씩 출력했다)
- get은 조건에 맞는 하나를 받고(0개도 에러가 난다), filter는 조건에 맞는 0개 ~ 여러개를 받는다.
- 이걸로 test를 쉽게 할 수 있다.
- 물론 admin 페이지는 더 쉽다.

## admin.py
- 되게 편하다..

# 겪은 오류와 해결 과정
- models.py를 패키지로 분리하여 두었는데, 이상하게 등록(마이그레이션)이 안됐다.
- \_\_init__파일에 임포트를 하지 않아서 생긴 문제였다.  
```python
from django.db import models
from .user import User, UserProfile

from .post import Post
from .comment import Comment
from .reply import Reply
from .category import Category
from .user_subject import UserSubject
from .subject import Subject
from .category import Category
from .subject_review import SubjectReview
```
- 모델들을 하나씩 임포트하였다.

# 궁금한 점

- 바로 위에랑 이어지는데, 저거 한번에 임포트하는 방법이 있나요?
- 그리고 위에도 언급했지만 시간표 time을 짜는 효율적인 방법이 무엇일까요?

# 새롭게 배운 점 

- ManyToManyField의 through 기능 (위에 언급하였음)
- CharField, TextField는 null=True보다 blank=True 쓸 것

# 느낀 점 및 회고
- 장고의 편의성은 파이썬을 따라간다(일단 파이썬이라 스트링 관리도 쉽다..)
- 뭔가 auth도 편할 것 같다(절대 인증/인가를 무시한 적 없습니다)
- 아직 간단한 모델들만 구현해서 그런지.. 장고의 편의성에 힘입어 빠르게 구현할 수 있었던 것 같다.
- 근데 간단한 모델 구현임에도 고려할게 생각보다 많았다.
- 커밋을 보면 번복이 꽤 많은데, 번복하지 않는 개발자가 되고싶다.


# CEOS 3주차 미션

## 미션 전에..
- 지난 주차 과제에서 아쉬웠던 점들을 개선해보자.

### BaseModel
- 모델들의 공통적인 필드들을 추출하여 모델을 만들어보자.
- 추출한 필드들은 다음과 같다.
    - created_at
    - updated_at
    - deleted_at
    - is_deleted

``` python
from django.db import models
from datetime import datetime


class BaseModel(models.Model):

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()
```
- soft delete를 구현하기 위해 delete 메소드를 오버라이딩 하였다.
- is_deleted 필드를 추가하여, 삭제 여부를 확인할 수 있도록 하였다.

### reply.py 제거
- 지난 주차에는 comment와 reply를 분리하였다.
- 하지만, comment에 parent 필드를 추가하여 reply를 대체하였다.

### 앱 단위 분리
- 지난 주차에선 models 패키지에 모델들을 모아놨다.
- 이번 주차에는 앱 단위로 분리해보자:
  - account: user, user_subject
  - post: post, comment, category
  - suject: subject, subject_review
- 앱 단위로 분리하니 임포트가 편해졌다.
- 생각보다 임포트가 어렵지도 않았다. 왜 진작 안했지

### AbstractUser
- 지난 주차에서 OneToOne method로 유저를 확장했다.
- 쿼리를 짜는 과정에서 비효율적이라고 판단했다.
- AbstractUser를 상속받아 확장했다.
> AUTH_USER_MODEL = "account.User"
- settings.py에 위와 같이 설정해주면 AbstractUser를 상속받은 User 모델을 사용할 수 있다.


## 목표
- CBV를 이용한 API 구현
- 나는 한 파일에 뭔가가 여러개 들어있는 꼴을 못보겠다.
- 노드 개발하면서 많이 데여서 그런 것 같다.
- 최대한 패키지로 만들어서 분리하였다.

### Serializer
- JSON <---> 객체 해주는 놈이다.
- 스프링의 Jackson과 비슷하다.

### api/views/subject_list_view.py
``` python
@csrf_exempt
def subject_list(request):
    """
    List all code subjects, or create a new subject.
    """
    if request.method == 'GET':
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SubjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
```
- 물론 'subject/subjects/' 로도 접근 가능하게 구현했다.
- 하지만 api 앱에서 여러 모델 관리를 하고자 한다.

### HTTP Status Code
- 보시면 JsonResponse에 status를 argument로 집어넣는다.
- 여러분은 200번대를 보면 행복하고, 400번대를 보면 불안해야 한다.
- 500번대는 없어야 한다. 600번대는 본 적이 없는데 안보고싶다.

#### Status Code List
- 200번대: 성공
  - 201: Created
- 300번대: 리다이렉트
- 400번대: 클라이언트 에러
  - 400: Bad Request
- 500번대: 서버 에러
- 600번대: 데이터베이스 에러

### 아무튼 PostMan을 이용해 API를 테스트해보자.
1. **GET** api/subjects/ 로 리스트를 모두 출력하자.
<img width="1013" alt="Screen Shot 2023-04-06 at 3 37 33 PM" src="https://user-images.githubusercontent.com/76674422/230291665-0a295f54-be94-40a2-8f4a-665402438fd4.png">

2. **GET** api/subjects/<id> 로 특정 subject를 출력하자.
<img width="1014" alt="Screen Shot 2023-04-06 at 3 38 15 PM" src="https://user-images.githubusercontent.com/76674422/230291827-a50b532f-22d9-4db2-b83a-a594243e59ca.png">

3. **POST** api/subjects/ 로 subject를 생성하자.
<img width="1013" alt="Screen Shot 2023-04-06 at 3 44 30 PM" src="https://user-images.githubusercontent.com/76674422/230293011-0d4b5f88-6886-46c4-b5ea-34e4abb17ef5.png">
- 난 무엇이든 해내

### ViewSet으로 리팩토링하기
- ViewSet은 View를 묶어주는 역할을 한다.
- '모든 데이터를 가져오는 API' 를 ViewSet으로 리팩토링하자.

api/views/subject_list_view.py
``` python
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
```

api/views/subject_detail_view.py
``` python
from rest_framework.viewsets import ModelViewSet
from subject.models import Subject
from subject.models.serializers import SubjectSerializer


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


subject_detail = SubjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
```
- 일단 PostMan으로 테스트 해봤는데, 잘 작동한다.
### 설명
- ModelViewSet은 Model과 Serializer를 기반으로 한다.
- queryset은 Model의 모든 객체를 가져온다.
- serializer_class는 Serializer를 가져온다.
- as_view()는 View를 가져온다.
- 'get': 'retrieve'는 GET 요청이 들어오면 retrieve 함수를 실행한다.
#### retrieve가 뭔데요
- retrieve는 ModelViewSet의 함수이다.
- GET posts/\<int:pk>/ 같이 특정 객체를 가져올 때 사용한다.

#### 어쨌든 작동이 잘 된다
- 그런데 지금 보이는 바와 같이, 중복된 코드가 너무 많이 나온다.

### 중복을 제거하자
- 1차 시도: __init__에 SubjectViewSet을 넣어주자.
  - 이렇게 하면 각각의 view에 SubjectViewSet이 들어가지 않는다. (import 문제)
  - 애초에 __init__은 로직 넣으라고 있는 파일이 아닌 것 같다.
  - 이런식으로 코딩하면 사장님이 월급을 안주신다.
- 2차 시도: subject_list_view.py에 SubjectViewSet을 넣어주자.

api/views/subject_detail_view.py
``` python
from .subject_list_view import SubjectViewSet

subject_detail = SubjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}) 
```
- 중복은 제거되었다.
- 근데 이렇게 하면 subject_list_view.py에 SubjectViewSet이 들어가게 된다.
- 나중에 view가 많아지면, SubjectViewSet을 넣을 위치를 정하는 근거를 뭘로 정해야 할까?
- (수정) 3차 시도: subject_view.py에 SubjectViewSet을 넣어주고 각각에 import 해준다.
- 이렇게 하는게 최선인 것 같다.

api/views/subject_list_view.py
```python
from .subject_view import SubjectViewSet


subject_list = SubjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
```
- 분리해서 두니 깔끔하죠?

### filter 기능 구현하기
- filterset을 이용해 filter 기능을 구현해보자.
- 요구사항:
  - 최소 하나의 필터는 method를 이용해 구현해 주세요
  - 문자열 단순 일치 이외의 필터링은 django ORM filter 기능을 활용하면 좋습니다👍


## FilterSet
> Django-filter는 view에 작성된 일반적인 코드를 계속 쓰는 부담을 덜어주는 일반적이고 재사용가능한 어플리케이션입니다. 구체적으로는 사용자들은 모델의 필드를 기반으로 queryset을 필터링 할 수 있습니다.
- 대충 '필터링 편한거' 라고 이해했다.
- model 패키지에 filter 패키지를 만들어보자.
- django_filters를 import하기 위해 django_filter를 설치해야 한다.
> $ pip install django-filter

api/views/subject_list_view.py
``` python
...
class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filterset_fields = ['subject_name', 'professor_name']
...
```
- `filterset_fields`를 이용해 필터링을 할 수 있다.
- *subject_name*과 *professor_name*으로 필터링이 가능하다.
- `SubjectViewSet` class 안에 `filterset_fields`를 넣어주는 이유는, 내부에 `queryset`이 모든 객체를 가져오기 떄문이다.
- 그래서 `filterset_fields`를 넣어주면, `queryset`을 필터링 할 수 있다.

### method를 이용해 필터링하기
- filterset_fields를 이용해 필터링을 할 수 있지만, 다양한 방법으로 필터링을 할 수 있다.
- 일단 현재 코드가 더러워졌다. (list_view에 필터 기능이 들어가있다)
- 제거 후 api/views/subject_filter_view.py를 만들어서 관리해보자.

api/views/subject_filter_view.py
``` python
from django_filters.rest_framework import FilterSet, filters


class SubjectFilter(FilterSet):
    subject_name = filters.CharFilter(lookup_expr='icontains')
    professor_name = filters.CharFilter(lookup_expr='icontains')
    is_cyber = filters.BooleanFilter(lookup_expr='exact')

    class Meta:
        fields = ['subject_name', 'professor_name', 'is_cyber']

    def filter_subject_name(self, queryset, name, value):
        return queryset.filter(subject_name__icontains=value)

    def filter_professor_name(self, queryset, name, value):
        return queryset.filter(professor_name__icontains=value)

    def filter_is_cyber(self, queryset, name, value):
        return queryset.filter(is_cyber=value)
```
- 초기 디자인 (밑에 수정하였다)

`lookup_expr` 는 필터링을 할 때, 어떤 방식으로 필터링을 할 것인지를 정해주는 것이다.
- `icontains`는 대소문자를 구분하지 않고, 문자열이 포함되어 있는지를 확인한다.
- `exact`는 대소문자를 구분하고, 문자열이 정확히 일치하는지를 확인한다.

- 근데.. DRF 필터 옵션에 is_cyber가 안보인다.. 왜지


## 오류 해결
- 문제점
  - `is_cyber` 필터링이 안된다.
  - method 방식을 사용하지 않는데 각각 필터의 메서드를 정의해두었다.



- 일단 디렉토리 리팩토링을 하였다.
  - views
    - \_\_init__.py
    - **subject_view.py**
    - subject_list_view.py
    - subject_detail_view.py
    - **subject_filter_view.py**

api/views/subject_view.py
```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from subject.models import Subject
from subject.models.serializers import SubjectSerializer
from .subject_filter_view import SubjectFilter


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter
    
```
- subject_list_view.py에 있던 `SubjectViewSet`을 subject_view.py로 옮겼다.
- SubjectViewSet에 filterset_class에 `SubjectFilter`를 넣어주었다.
- `SubjectFilter`는 subject_filter_view.py에 있다.

api/views/subject_filter_view.py
```python
from django_filters.rest_framework import FilterSet, filters
from subject.models import Subject


class SubjectFilter(FilterSet):
    subject_name = filters.CharFilter(lookup_expr='icontains', label='과목명')
    professor_name = filters.CharFilter(lookup_expr='icontains', label='교수명')
    is_cyber = filters.BooleanFilter(method='is_cyber_filter', label='비대면 여부')

    class Meta:
        model = Subject
        fields = ['subject_name', 'professor_name', 'is_cyber']

    def is_cyber_filter(self, queryset, name, value):
        return queryset.filter(is_cyber=value)
```
- is_cyber_filter method를 만들어서 구현했다
- 오류 해결! 다 잘 작동한다. 그런데..

```python
from django_filters.rest_framework import FilterSet
from subject.models import Subject


class SubjectFilter(FilterSet):
    class Meta:
        model = Subject
        fields = ['subject_name', 'professor_name', 'is_cyber']
```
- 이렇게만 둬도 잘 작동한다.

<img width="1440" alt="Screen Shot 2023-04-07 at 6 53 04 PM" src="https://user-images.githubusercontent.com/76674422/230588273-f524f8f3-f768-4df8-a57d-5f3ecb97d70c.png">
- 그럼 왜 굳이 따로 명시해뒀지??

### filters.Filter의 argument로 속성 부여
- `subject_name`과 `professor_name`은 `lookup_expr`를 이용해 필터링을 하였다.
- 이렇게 하면 '**정확히 일치하는 문자**'가 아닌 '**포함하는 문자**'를 검색할 수 있다.
- ex) '어셈' 만 쳐도 '어셈블리언어및실습'을 검색할 수 있다.

<img width="1440" alt="Screen Shot 2023-04-07 at 7 57 02 PM" src="https://user-images.githubusercontent.com/76674422/230597412-bb1ce497-cbd3-40fa-acf0-cc08fe4ad4c3.png">

- 사진은 없지만 DRF에서 POST도 잘 동작하는걸 확인했다.

### method로 필터링 커스텀
- method를 이용하면 좀 더 특별한 필터링이 가능할 것 같다. (ex: 일정 좋아요 수를 넘는 댓글 display)


# 후기
- 생각보다 할 게 많았다. 
- 모든 기능들에 대한 view, filter를 구현할 수 있겠지만.. 시간상.. 하지 못했다.
### DRF with Browser
- 솔직히 PostMan을 써온 사람으로서, 처음엔 DRF 브라우저 기능에 대한 반감이 있었다. (PostMan과의 의리)
- 근데 DRF 브라우저 기능이 너무 편하다.
- admin 페이지도 그렇고, 개발자를 잘 챙겨주는 모습에 감동했다.
### Overall
- 그럼 이제 '최소한의 장고'에 대해 이해한 것 같다.
- 걱정이 된다. 배포 과제 잘 마칠 수 있을까..?
<img width="707" alt="Screen Shot 2023-04-07 at 7 53 05 PM" src="https://user-images.githubusercontent.com/76674422/230596998-16e435e1-3360-4864-9c93-1b636298ea3a.png">
