from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.admin.promo.views import PromoAdminViewSet, PromoPurchasedAdminView

router = DefaultRouter()
router.register(r'', PromoAdminViewSet, basename='admin-promo')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/purchased/',  PromoPurchasedAdminView.as_view(), name='admin-promo-purchased'),
    path('purchased/<int:id>/',  PromoPurchasedAdminView.as_view(), name='admin-promo-purchased-delete'),
]