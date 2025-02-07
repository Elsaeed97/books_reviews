from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, UserDetailView

app_name = 'users'

urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', UserDetailView.as_view(), name='user_detail'),
]