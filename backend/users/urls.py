from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GameViewSet, PlayerSettingsViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'games', GameViewSet, basename='games')
router.register(r'player-settings', PlayerSettingsViewSet, basename='player-settings')

urlpatterns = [
    path('', include(router.urls)),
]
