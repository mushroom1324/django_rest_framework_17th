from django.contrib import admin

from .models import User, UserSubject
# Register your models here.

admin.site.register(User)
admin.site.register(UserSubject)

