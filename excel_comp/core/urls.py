from django.urls import path

from . import views

urlpatterns = [
    path('',views.HomepageView.as_view(),name='home'),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('about/',views.AboutView.as_view(),name='about'),
    path('support/',views.SupportView.as_view(),name='support'),
    path('cookies policy/',views.CookiesView.as_view(),name='cookies'),
    path('privacy/',views.PrivacyView.as_view(),name='privacy'),
    path('how_to_use/',views.HowToUseView.as_view(),name='how_to_use'),
]