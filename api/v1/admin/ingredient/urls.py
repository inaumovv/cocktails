from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.admin.ingredient.views import AdminIngredientViewSet, AdminIngredientCategoryViewSet, \
    AdminIngredientCategorySectionViewSet

router = DefaultRouter()
router.register(r'', AdminIngredientViewSet, basename='admin-ingredient')
router.register(r'category', AdminIngredientCategoryViewSet, basename='admin-ingredient-category')
router.register(r'category-section', AdminIngredientCategorySectionViewSet, basename='admin-ingredient-category-section')

urlpatterns = [
    path('', include(router.urls)),
]