# Shell Commands

## Create User model
``` shell
cd ..
cd ..
python manage.py shell
from django.db import models
from api.models.user import User, UserProfile
from api.models.post import Post
from api.models.comment import Comment
from api.models.reply import Reply
from api.models.category import Category
from api.models.user_subject import UserSubject
from api.models.subject import Subject
from api.models.category import Category
user1 = User.objects.create_user(username='mushroom1324', password='password', first_name='서', last_name='찬혁', email='mushroom1324@naver.com')
user2 = User.objects.create_user(username='takgyun', password='password2', first_name='임', last_name='탁균', email='takgyun@naver.com')
user3 = User.objects.create_user(username='someone', password='password3', first_name='홍', last_name='길동')
```

## Filter Non-staff User(s) and display
``` shell
cd ..
cd ..
python manage.py shell
from django.db import models
from api.models.user import User, UserProfile
from api.models.post import Post
from api.models.comment import Comment
from api.models.reply import Reply
from api.models.category import Category
from api.models.user_subject import UserSubject
from api.models.subject import Subject
from api.models.category import Category
non_staffs = User.objects.filter(is_staff=0)
for account in non_staffs:
    print("Username:", account.username)
    print("Email:", account.email)
    print("Password:", account.password)
    print("###########################")

```

## List User Models
``` shell
cd ..
cd ..
python manage.py shell
from django.db import models
from api.models.user import User, UserProfile
from api.models.post import Post
from api.models.comment import Comment
from api.models.reply import Reply
from api.models.category import Category
from api.models.user_subject import UserSubject
from api.models.subject import Subject
from api.models.category import Category
User.objects.all()
    
```

## List User Friend Lists
``` shell
cd ..
cd ..
python manage.py shell
from django.db import models
from api.models.user import User, UserProfile
from api.models.post import Post
from api.models.comment import Comment
from api.models.reply import Reply
from api.models.category import Category
from api.models.user_subject import UserSubject
from api.models.subject import Subject
from api.models.category import Category
user1 = User.objects.get(pk=6)
user_profile1 = UserProfile.objects.get(user=user1) 
user_profile1.friend_list.all()
```

