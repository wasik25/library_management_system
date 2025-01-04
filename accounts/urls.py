from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, DepositView, profile_view
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('deposit/', DepositView.as_view(), name='deposit'),
]
