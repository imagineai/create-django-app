from django.contrib import admin

from .models import Todo
from .user import User

admin.site.register(Todo)
admin.site.register(User)
