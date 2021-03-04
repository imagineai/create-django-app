from django.contrib import admin

from .models import Comment, Person, Todo
from .user import User

admin.site.register(Todo)
admin.site.register(Comment)
admin.site.register(Person)
admin.site.register(User)
