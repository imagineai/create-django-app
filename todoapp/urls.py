from django.conf.urls import include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, CreatePersonViewSet, TodoViewSet

router = DefaultRouter()

router.register(r'todo', TodoViewSet, 'todo')
router.register(r'comment', CommentViewSet, 'comment')
router.register(r'create_person', CreatePersonViewSet, 'create_person')

schema_view = get_schema_view(
    openapi.Info(
        title="todoapp",
        default_version='v1',
        description="API description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path('^', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
