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
- 
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
from subject.serializers import SubjectSerializer
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
- method를 이용하면 좀 더 특별한 필터링이 가능할 것 같다. (ex: 핫게 필터 뭐 이런..)


# 후기
- 생각보다 할 게 많았다. 
- 모든 기능들에 대한 view, filter를 구현할 수 있겠지만.. 시간상.. 하지 못했다.
- 솔직히 전부 뭐 패키지 분리 안하고 한꺼번에 박아뒀으면 금방 했을 것 같다.
- 그래도 뭐.. 하고 보니 깔끔해뵈긴 하다 ㅎㅎ

### DRF with Browser
- 솔직히 PostMan을 써온 사람으로서, 처음엔 DRF 브라우저 기능에 대한 반감이 있었다. (PostMan과의 의리)
- 근데 DRF 브라우저 기능이 너무 편하다.
- admin 페이지도 그렇고, 개발자를 잘 챙겨주는 모습에 감동했다.
### Overall
- 그럼 이제 '최소한의 장고'에 대해 이해한 것 같다.
- 걱정이 된다. 배포 과제 잘 마칠 수 있을까..?
<img width="707" alt="Screen Shot 2023-04-07 at 7 53 05 PM" src="https://user-images.githubusercontent.com/76674422/230596998-16e435e1-3360-4864-9c93-1b636298ea3a.png">

# 피드백 반영하기
> 피드백 주셔서 감사합니다.. 이제 시험도 끝났겠다 수정하겠습니다

#### _현재는 deleted_at과 is_deleted가 둘다 보이는데, deleted_at 값이 null이 아니라면 delete된 것으로 판단할 수 있기 때문에 둘 중 하나만 이용하셔도 soft delete를 구현하실 수 있습니다!_

- 그래서.. is_deleted를 삭제했습니다.

**base_model.py**
```python
class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now()
        self.save()
```
- 감사합니다.

## _이 방식은 CBV가 아니라 FBV 아닌가요?_
- 헉
### FBV (Function-Base Views)
- FBV는 함수 기반의 뷰이다.
- 장점: 
  - 구현의 단순함
- 단점: 
  - 재사용성이 떨어짐
  - 조건문으로 HTTP 메소드를 구분

### CBV (Class-Base Views)
- CBV는 클래스 기반의 뷰이다.
- 장점: 
  - HTTP 메소드에 대한 처리를 조건문이 아닌 메소드 명으로 구분하여 코드가 깔끔
  - 제너릭 뷰, 믹스인 클래스 등을 사용해 코드의 재사용성, 개발 생산성을 높여줌

<br>
api/의 view는 CBV로 되어있지만 APIView는 쓰지 않았다
다른 앱들의 view는 FBV로 되어있다. 
그래서 CBV - APIView로 통일하였다.

```python
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
```
- 감사합니다.
- 잘 작동하는데, DRF 페이지에 있던 Filter 버튼이 없어졌다..
- 뭐.. 그래도 잘 작동하는 것 같다.



### _지금 api가 'post/posts/' 이런 식인 것 같은데 restful한 api를 설계하기 위해서 컨벤션을 잘 지키면 좋을 것 같아요!!_

- 현재 api/subjects/ 로 접근하여 HTTP요청을 할 수 있습니다!
- 하지만 subject, post app 내의 urls.py를 보면 post/post 이런식으로 되어있습니다.
- 프로젝트의 urls.py를 보면 다음과 같이 고칩니다.

```python
urlpatterns = [
    path('accounts/', include('account.urls')),
    path('posts/', include('post.urls')),
    path('subjects/', include('subject.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
```

- 그리고 각각의 app의 url을 다음과 같이 고칩니다.
post/urls.py
```python
urlpatterns = [
    path('', views.PostList.as_view()),
]
```
- 이제 `http://localhost:8080/posts/` 로 접근할 수 있습니다.
- 감사합니다.

## Soft deletion
- 깜빡 잊고있었는데 이것도 해봤다.
- 다양한 방법이 있는데, 외부 라이브러리 `safedelete`를 사용해봤다.

https://django-safedelete.readthedocs.io/en/latest/models.html

``` python
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class Subject(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    subject_name = models.CharField(max_length=255)
    professor_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location_info = models.CharField(max_length=255, blank=True)
    time = models.TextField(blank=True)

    is_cyber = models.BooleanField(default=False)

    def __str__(self):
        return self.subject_name
```
- 이렇게 하면, `delete()` 메소드를 사용할 때, `deleted_at`에 현재 시간이 저장된다.

<img width="613" alt="Screen Shot 2023-04-28 at 1 37 53 PM" src="https://user-images.githubusercontent.com/76674422/235055419-43246fde-1a7a-46a4-b4d2-70cd3b24f46b.png">

- 난 무엇이든 해내

- 근데 이렇게 하는거 별로 안좋은 것 같긴 하다. 내가 구현하면 되는데 굳이 이걸 왜 쓰지
- SafeDeleteModel을 상속받는것도 유연성이 떨어져서 별로인 것 같다. (AbstractUser를 상속받는 account model에는 어떻게 적용할 것인가?)
- 그래서 직접 구현하기로 했다~

```python
from django.db import models
from api.models.base_model import BaseModel
from datetime import datetime


class Subject(BaseModel):
    subject_name = models.CharField(max_length=255)
    professor_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location_info = models.CharField(max_length=255, blank=True)
    time = models.TextField(blank=True)

    is_cyber = models.BooleanField(default=False)

    def __str__(self):
        return self.subject_name

    # implement safe delete
    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now()
        self.save()     
```
- 이렇게 해두니 deleted_at이 잘 작동한다.
- 그럼 이제 list를 불러올 때 deleted_at이 널인 것들만 불러오면 되겠다.

```python
    @staticmethod
    def get(request):
        # get objects which are not deleted
        subjects = Subject.objects.filter(deleted_at__isnull=True)
        filtered_subjects = SubjectFilter(request.GET, queryset=subjects)
        serializer = SubjectSerializer(filtered_subjects.qs, many=True)
        return Response(serializer.data)
```
- 짜잔
- 모두 잘 동작하는것을 확인하였다.

- 가 아니고! 바보같은 실수를 했는데
- BaseModel에 delete 메소드 잘 구현해놓고 상속하는 Subject에 또 delete 메소드를 구현했다 ..
- 이러면 어떻게 될까?
- 그렇다. 상속하는 Subject 모델의 delete에 우선권이 주어진다.(오버라이딩)
- 하지만 아무것도 확장하지 안하는 단순 중복 코드는 필요없으므로 삭제했다.
```python
class Subject(BaseModel):
    subject_name = models.CharField(max_length=255)
    professor_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location_info = models.CharField(max_length=255, blank=True)
    time = models.TextField(blank=True)

    is_cyber = models.BooleanField(default=False)

    def __str__(self):
        return self.subject_name
```

### 자 그럼 이제 라이브러리를 삭제해야한다.

- `pip uninstall django-safedelete` 를 통해 삭제하였다. (설마 이것도 safe delete 되나)
- INSTALLED_APPS에서도 safedelete를 삭제했다.

## 피드백 반영 후 느낀점
- CBV방식이 구현하기 더 어렵다
- 하지만 해냈다
- 페이지네이션도 구현해두면 좋겠다. (나중에)
- 끝~






# 4주차 미션

로그인 구현하기

# 이론

- 세션 방식과 토큰 방식이 있습니다.
- 저희에게 중요한 것은 보안성과 효율성이므로 두개의 측면에서 바라보겠습니다.

## 세션

- 세션 정보를 쿠키에 담아 소통하고, 인증 정보를 서버에 둡니다.
- 서버에 저장되는 세션 정보는 서버 메모리에 저장되거나, DB에 저장됩니다.
- 사실 세션의 경우 쿠키 헤더에 ID만 담아서 보내면 되므로 트래픽을 적게 먹습니다. (효율 좋음)
- 세션 ID가 탈취당해도 서버측에서 세션을 무효처리 하면 됩니다. (보안성 좋음)

#### 왜 안씀?

- 확장성이 문제입니다..
- 세션은 Stateful 합니다. (서버에 저장되어야 하므로)
- 서버가 여러대라면 세션을 공유해야겠죠? (DB를 공유하거나, Redis를 사용하거나)
- 이러면 서버가 늘어날수록 세션을 공유해야하는 부담이 생깁니다.
- 저희가 장난삼아 만드는 사이트엔 세션도 부담이 없겠지만, 서버 규모가 커질수록 이러한 세션방식의 한계가 생길겁니다.
- Stateless한 토큰 방식을 사용합시다. (JWT)

## 토큰

- 위에서 말했듯 Stateless합니다.
- 토큰은 인증 정보를 클라이언트에게 줍니다.

#### Access Token

- 클라이언트가 ID/PW를 넘겨주면 서버는 Access Token을 반환해줍니다.
- 이 토큰은 전자서명이 되어있습니다. (토큰의 훼손 방지)
- Access Token 자체가 인증 정보이기 때문에, Stateless 합니다.
- 하지만 토큰을 탈취당한다면, 토큰이 만료될 때까지 탈취한 사람이 인증을 할 수 있습니다.
- 그렇기 때문에 Access Token은 만료시간을 짧게 가져가야합니다.
- 그치만 만료시간이 짧으면 만료될때마다 로그인을 해줘야겠죠?
- 그래서 Refresh Token이 등장합니다.

#### Refresh Token

- 클라이언트가 로그인 시 Access Token을 넘겨주면서 Refresh Token도 같이 줍니다.
- 서버는 DB에 Refresh Token을 저장합니다.
- 클라이언트는 Access Token 만료 시 받아뒀던 Refresh Token을 이용해 Access Token 재발급을 요청합니다.
- 서버는 DB에 저장된 Refresh Token과 클라이언트가 보낸 Refresh Token을 비교하고 일치하면 Access Token을 재발급합니다.
- 물론 Refresh Token도 탈취 가능성이 있지만 만료시간이 길기 때문에 Access Token보다는 안전합니다.


# 실습


## django rest framework JWT 설치

> pip install djangorestframework djangorestframework-jwt

> pip freeze > requirements.txt

## settings.py에 추가
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_SECRET_KEY': env('JWT_SECRET_KEY'),
    'JWT_ALGORITHM': 'HS256',
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),
}
```
간략한 설명..

`DEFAULT_PERMISSION_CLASSES`
- `rest_framework.permissions.IsAuthenticated` 로 로그인 판별

`DEFAULT_AUTHENTICATION_CLASSES`
- `rest_framework_jwt.authentication.JSONWebTokenAuthentication` 즉 JWT 사용하겠다고 선언

`JWT_SECRET_KEY`
- 암호화시 사용하는 비밀 키로, .env에 저장하는게 좋아보입니다.

`JWT_ALGORITHM`
- "JWT 암호화에 어떤 알고리즘을 사용할거냐" 입니다. HS256 사용하겠습니다.

`JWT_ALLOW_REFRESH`
- 리프레쉬 토큰 쓸거니까 True로 둘게요.

`JWT_EXPIRATION_DELTA`
- 토큰의 유효기간입니다. 갱신하지 않을 시 토큰은 7일 후 만료됩니다. 
- 왜 7일이냐: 솔직히 구글링하면서 따라한거라.. 하란대로 7일 넣었습니다. 다들 그렇게 했잖아요.

`JWT_REFRESH_EXPIRATION_DELTA`
- 토큰 갱신의 유효기간입니다. 토큰은 최대 28일까지 갱신 후 무조건 만료됩니다.

## URL 설정
<img width="772" alt="image" src="https://user-images.githubusercontent.com/76674422/235585719-d94becc9-8332-49e1-9074-98b1926cdc79.png">
<div>제가 본 블로그인데요.. url을 저렇게 configure 해놨더라구요.</div>
<div>저는 이미 api 앱이 있으니, api 앱 안에 넣겠습니다.</div>

api/urls.py
```python
from django.urls import path
from api import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    path('subjects/', views.SubjectListViewSet.as_view()),
    path('subjects/<int:pk>/', views.SubjectDetailViewSet.as_view()),
    path('login/', obtain_jwt_token),
    path('login/verify/', verify_jwt_token),
    path('login/refresh/', refresh_jwt_token),
]
```
`obtain_jwt_token`
- 발행

`verify_jwt_token`
- 검증

`refresh_jwt_token`
- 갱신

## Views 설정
<div>만들어둔게 subject 모델 관련이니, _과목들을 보려면 서버가 인가해주어야 한다_ 라고 가정할게요.</div>
<div>제가 본 블로그 페이지는 FBV를 썼더라구요. 눈치껐 했습니다.</div>

api/views/subject_list_view.py
```python
    @staticmethod
    @api_view(['GET']) # 지웠음
    @permission_classes([IsAuthenticated])
    @authentication_classes([JSONWebTokenAuthentication])
    def get(request):
        # get objects which are not deleted
        subjects = Subject.objects.filter(deleted_at__isnull=True)
        filtered_subjects = SubjectFilter(request.GET, queryset=subjects)
        serializer = SubjectSerializer(filtered_subjects.qs, many=True)
        return Response(serializer.data)
```
<div>데코레이터 3개가 추가됐습니다.</div>

`@api_view(['GET'])`
- GET 요청만 받겠다고 선언하는건데 이미 잘만 쓰던건데 굳이 싶어서.. 뺐습니다.

`@permission_classes([IsAuthenticated])`
- 권한을 체크하는 곳입니다.

`@authentication_classes([JSONWebTokenAuthentication])`
- JWT 토큰을 확인합니다. 토큰에 이상이 있으면 에러를 JSON으로 던집니다.

<div>근데 이상하죠.. 말만 들으면 permission_classes나 authentication_classes나 둘다 권한체크입니다..</div>
<div>권한 체크하려면 당연히 JWT 토큰을 확인해야 하는 것 아닐까요</div>

<div>그래서 Stack Overflow에서 괜찮은 답변을 찾았습니다..</div>

>After removing TokenAuthentication class you are able to access the api because then drf is using session authentication and browser handles the sessions for you. When you use TokenAuthentication then you need to add token in header of request which is not done by browser. thats why you are getting { "detail": "Authentication credentials were not provided." }. try this api from postman by adding the token in headers then it will work.

- `@authentication_classes([JSONWebTokenAuthentication])` 이 없다면 DRF는 세션 인증을 사용합니다.
- 제가 `@authentication_classes([JSONWebTokenAuthentication])`를 없애보겠습니다.
<img width="772" alt="image" src="https://user-images.githubusercontent.com/76674422/235589879-de7737fe-f829-473f-abcf-f7ac1886a57f.png">
- ?
- 계획대로면 JWT 얘기가 없고 세션 얘기가 나와야 하는데 그쵸
- 아니 뭐 해보는김에 원복 후 `@permission_classes([IsAuthenticated])` 를 빼고 해봤습니다.

<img width="772" alt="image" src="https://user-images.githubusercontent.com/76674422/235590484-85f0e56a-958b-4ae5-b6b4-906b9985627d.png">

- ??
- 진짜 뭐 둘이 역할이 똑같나요?
- 그럼.. 그럼 둘 다 빼보겠습니다.

<img width="772" alt="image" src="https://user-images.githubusercontent.com/76674422/235591152-c1e79232-662a-4e0a-8f1e-3d546e9db4b7.png">

- ㅋㅋㅋㅋㅋ
- 아 이게 왜 이런가 했더니 default값이 settings.py에 있는 값을 따르기 때문이라고 하네요..
- 바보가 된 기분이었습니다. 역시 스택 오버플로우 형님들은 거짓말을 하지 않습니다.


### 유용한 정보
- `@permission_classes` 는 HTTP 403 에러를 던집니다.
- `@authentication_classes` 는 HTTP 401 에러를 던집니다.
- settings.py에 있는 `'rest_framework_jwt.authentication.JSONWebTokenAuthentication'`을 주석처리하면 DRF가 세션 로그인 방식으로 감지하고 **403** 에러를 던집니다.
- 왜냐면 `@authentication_classes`가 세션 로그인 방식으로 감지하기 때문에 **헤더의 JWT토큰을 찾지 않고** 그냥 넘기기 때문입니다.
- 그러면 `@permission_classes`가 로그인이 되어있지 않은걸 확인하고 에러를 던지기 때문에 그렇습니다.
- 이제 각각이 다른 놈인걸 인지했죠?
- 자 그럼 좀 더 세밀하게 테스트합시다.

### 테스트 via Postman
<img width="1033" alt="image" src="https://user-images.githubusercontent.com/76674422/235593673-8daef165-aff2-4793-9440-9c84513f1afb.png">

- 로그인 하니까 토큰 잘 주죠
- 아까 말했듯이, 이 토큰을 헤더에 담아서 쓰면 7일동안 잘 쓸 수 있다는거죠.

<img width="1033" alt="image" src="https://user-images.githubusercontent.com/76674422/235596351-a54eb286-c577-4e4d-b99b-69edb11a50bd.png">

- 방금 받은 토큰을 헤더에 담아서 subject get 요청을 하니 잘 줍니다.

<img width="1033" alt="image" src="https://user-images.githubusercontent.com/76674422/235608611-3cb84569-483b-434a-b7e6-fce3d5f10d88.png">

- verify가 잘 되는 모습입니다.

<img width="1033" alt="image" src="https://user-images.githubusercontent.com/76674422/235608752-d7fe8f5e-3cce-451c-b9a5-2d3e7fea389a.png">

- refresh가 잘 되는 모습입니다.

# 다시
- 아 Simple JWT를 써야겠다고 판단하고 다 지우고 다시 합니다..
- 왜 다시했나요: 할 말이 많습니다.. 결론적으로 Simple JWT가 구현에 더 유리하다고 판단하여 처음부터 다시 시작했습니다.
- django rest framework JWT 쓰니까 superuser만 잘 작동하고 일반 유저 접근이 잘 안되더라구요..
- 물론 가능하겠지만 전 실패했습니다.
- 아무튼 화나서 다 버리고 다시 했습니다.
- 화가 너무 나서 커밋 메세지도 '다시' 로 했습니다..
- 설정 방법은 비슷하고, 여러 시행착오 끝에 서버에 회원가입/로그인 한 유저에게 토큰을 줄 수 있었습니다

![image](https://user-images.githubusercontent.com/76674422/236623964-052b5b38-2860-4b11-9adc-8f2a753e2eec.png)

- 이론 쪽에서 말씀드렸듯이 로그인 시 엑세스 토큰과 리프레시 토큰을 줍니다.

![image](https://user-images.githubusercontent.com/76674422/236624085-e1e01228-b96a-4184-9708-413b70d11c58.png)

- 회원가입/로그인 시 받은 리프레시 토큰으로 리프레시 url에 접근하면 저렇게 엑세스 토큰을 재발급해줍니다.

- 리프레시 토큰 발급은 simple jwt의 내장 기능을 이용했습니다. (사실 토큰 발급도 내장 기능을 이용한거죠..)


```python

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class LoginAPIView(APIView):
    @staticmethod
    def post(request):
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
```

- authenticate()는 유저 정보(email, password)를 받아서 유저가 valid한지 체크해줍니다.
- valid하면 (not None) 토큰을 갖다줍니다.
- 그렇지 않으면 400 에러를 던집니다.

# 로그아웃?
- 토큰이 만료되면 로그아웃됩니다.
- 만료되기 전에 로그아웃하고 싶다면, 토큰을 블랙리스트에 추가하면 됩니다.

`'rest_framework_simplejwt.token_blacklist',` 를 settings.py에 추가해줍니다.

```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        try:
            refresh_token = request.COOKIES.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
```
- 저렇게 블랙리스트에 토큰을 추가해주면 됩니다.

![image](https://user-images.githubusercontent.com/76674422/236626013-85d0047f-de2b-40ef-a14c-ea2794bb6573.png)

- 짜잔

# 권한 설정
- 위에서 스포를 살짝 했습니다.
- 그렇습니다. `permission_classes = (IsAuthenticated,)` 로 권한 설정을 하면 됩니다.
- 이렇게 하면 로그인한 유저만 접근할 수 있습니다.
- 해당 url에 접근하려면 헤더에 Authorization : token을 담아서 보내야 합니다

# 겪은 오류와 해결

```python
    # staticmethod면 self 빼야함
    @staticmethod
    def post(request):
    
    # staticmethod 안쓰면 self도 넣음 
    def post(self, request):
```
- 일단 이게 저를 진짜 미치게 했습니다.
- 저기 아래처럼 post에 staticmethod 안써두면 노란 밑줄 생기면서 staticmethod로 쓰라고 하거든요?
- 근데 그거 쓰면 self를 뺴야합니다. 안그러면 request를 못받았다고 post가 안됩니다..
- 제가 예전에 postman 쓰다가 post 메서드를 잘못 건드린 적 있어서 postman 문젠가? 싶어가지고 막 재설치 하고 죄없는 DB 갈아엎고 난리도 아니었습니다
- 결국 저거 하나 문제였네요. (에러메세지도 너무 포괄적 메세지라 구글링도 안되고 .. . ...)
- 사실 이거 많고도 문제가 많았는데요, 너무 많아서 기억이 나질 않습니다

# 후기
- django rest framework JWT 때문에 너무 화가 났습니다.
- 어쨌든.. 해냈습니다
- Simple JWT 화이팅입니다.

