from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .jwt_views import CustomTokenObtainPairView
from .views import (
    RegisterView, login_view, UserProfileView, 
    get_user_stats, get_user_by_id, get_user_rating
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('stats/', get_user_stats, name='user-stats'),
    path('<uuid:userId>/', get_user_by_id, name='get-user-by-id'),
    path('<uuid:userId>/rating/', get_user_rating, name='get-user-rating'),
]
