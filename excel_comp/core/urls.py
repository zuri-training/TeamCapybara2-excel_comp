from django.urls import path

from . import views

urlpatterns = [
    path('',views.HomepageView.as_view(),name='home'),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),
]