from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminConfigViewSet

router = DefaultRouter()
router.register(r'', AdminConfigViewSet, basename='admin-config')

urlpatterns = [
    path('', include(router.urls)),
]