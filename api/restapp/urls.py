
from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import AuthTestView, AlbumView, AlbumDetail, ArtifactView, ArtifactDetail, AlbumPageView, AlbumPageDetail

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/authcheck/', AuthTestView.as_view(), name='test-auth'),
    re_path('api/album/?$', AlbumView.as_view(), name='album-list'),
    path('api/album/<int:pk>', AlbumDetail.as_view(), name='album-detail'),
    re_path('api/artifact/?$', ArtifactView.as_view(), name='artifact-list'),
    path('api/artifact/<int:pk>', ArtifactDetail.as_view(), name='artifact-detail'),
    re_path('api/album_page/?$', AlbumPageView.as_view(), name='album-page-list'),
    path('api/album_page/<int:pk>', AlbumPageDetail.as_view(), name='album-page-detail'),
]
