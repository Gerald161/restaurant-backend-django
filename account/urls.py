from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('signup', views.signup.as_view()),
    path('api/token', obtain_auth_token, name="obtain-token"),
    path('login', views.loginView.as_view()),
    path('logout', views.logoutView.as_view()),
    path('api/change-password/', views.changePasswordView.as_view(), name='change-password'),
    path('accountUserDetails', views.accountUserDetails.as_view(), name="account_user_details"),
    path('updateUserDetails', views.updateUserDetails.as_view(), name="change_user_details"),
    path('deleteAccount', views.deleteAccount.as_view()),
    path('sendResetPasswordToken', views.sendResetPasswordToken.as_view()),
    path('resetPasswordWithToken', views.resetPasswordWithToken.as_view()),
    path('removeExpiredTokens', views.removeExpiredTokens.as_view()),


    path('reset_password/', auth_views.PasswordResetView.as_view()),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
]
