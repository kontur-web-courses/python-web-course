from django.contrib import admin
from django.urls import path, include
from projects.views import ProjectViewSet
from tasks.views import TaskViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
]
