from django.urls import path,re_path
# from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.LoginView.as_view(),name='login'),
    path('',views.logout_user,name='logout'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('verify/',views.AccountValidationView.as_view(),name='verify_account'),
    

    # Authentication Views
    # path('home',views.home,name='home'),
    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]



# 'password_reset_confirm