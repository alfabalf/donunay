
from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import AuthTestView, AlbumView, AlbumDetail


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/authcheck/', AuthTestView.as_view(), name='test-auth'),
    re_path('api/album/?$', AlbumView.as_view(), name='album-list'),
    path('api/album/<str:_uuid>', AlbumDetail.as_view(), name='album-detail'),
]
