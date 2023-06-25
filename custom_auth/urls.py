from django.urls import path
from custom_auth.views import RegistrationView, EmailVerificationView, LoginView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('email-verify/<str:uid>/<str:token>/', EmailVerificationView.as_view(), 
         name='email-verify'),
    path('login/', LoginView.as_view(), name='login'),
]