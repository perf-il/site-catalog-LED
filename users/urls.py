from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, wait_confirm_email, ConfirmPage, UserForgotPasswordView, \
    UserPasswordResetDoneView, UserPasswordResetConfirmView

app_name = UsersConfig.name

urlpatterns = [
    path('/login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('/logout', LogoutView.as_view(), name='logout'),
    path('/register', RegisterView.as_view(), name='register'),
    path('/profile', ProfileView.as_view(), name='profile'),
    path('/wait-confirm-email', wait_confirm_email, name='confirm_email'),
    path('/confirm_email/<int:pk>', ConfirmPage.as_view(), name='confirmed_email'),
    path('/password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('/set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('/password-reset-sent/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('/password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
