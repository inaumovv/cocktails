from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminPointViewSet

router = DefaultRouter()
router.register(r'', AdminPointViewSet, basename='admin-point')

urlpatterns = [
    path('', include(router.urls)),
]