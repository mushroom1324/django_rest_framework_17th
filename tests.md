
### Test user_serializer
``` shell

python manage.py shell

from account.models import User
from account.models.serializers import UserSerializer

user = User.objects.get(username='test')
serializer = UserSerializer(user)
serializer.data

```

### Test category_serializer
``` shell

python manage.py shell

from post.models import Category
from post.models.serializers import CategorySerializer

category = Category.objects.get(name='test')
serializer = CategorySerializer(category)
serializer.data

```

### Test post_serializer
``` shell

python manage.py shell

from post.models import Post
from post.models.serializers import PostSerializer

post = Post.objects.get(category__name='컴퓨터공학과')
serializer = PostSerializer(post)
serializer.data

```

