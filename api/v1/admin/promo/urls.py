from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.admin.promo.views import PromoAdminViewSet, PromoPurchasedAdminViewSet

router = DefaultRouter()
router.register(r'', PromoAdminViewSet, basename='admin-promo')
router.register(r'purchased', PromoPurchasedAdminViewSet, basename='admin-purchased-promo')

urlpatterns = [
    path('', include(router.urls)),
]
