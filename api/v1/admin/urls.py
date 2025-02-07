from django.urls import path, include

app_name = 'admin_api'

urlpatterns = [
    path('goods/', include('api.v1.admin.goods.urls')),
    path('recipe/', include('api.v1.admin.recipe.urls')),
    path('profile/', include('api.v1.admin.profile.urls')),
    path('point/', include('api.v1.admin.point.urls')),
    path('sup/', include('api.v1.admin.support.urls')),
    path('auth/', include('api.v1.admin.auth.urls')),
    path('config/', include('api.v1.admin.config.urls')),
]
