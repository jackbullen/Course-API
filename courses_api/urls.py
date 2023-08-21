from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from courses import views

# setup docs
schema_view = get_schema_view(
   openapi.Info(
      title="UVic Courses API",
      default_version='v1',
      description="Endpoints for UVic course scheduling.",
      terms_of_service="https://www.uvic.ca/info/terms-of-use/index.php",
      contact=openapi.Contact(email="jackbullen@uvic.ca"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# setup urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),
    path('', views.index, name='index'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
