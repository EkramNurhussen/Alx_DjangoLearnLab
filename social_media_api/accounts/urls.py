# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowViewSet

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowViewSet.as_view({'post': 'follow'}), name='follow'),
    path('unfollow/<int:user_id>/', FollowViewSet.as_view({'post': 'unfollow'}), name='unfollow'),
]