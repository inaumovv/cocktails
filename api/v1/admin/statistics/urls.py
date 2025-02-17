from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminStatisticsViewSet


router = DefaultRouter()
router.register(r'', AdminStatisticsViewSet, basename='admin-statistics')

urlpatterns = [
    path('', include(router.urls)),
]