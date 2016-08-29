from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^signup/$', views.user_signup, name="signup"),
    url(r'^login/$', views.user_login, name="login"),
    url(r'^reset_password/', views.ResetPasswordRequestView.as_view(), name="reset_password"),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
]