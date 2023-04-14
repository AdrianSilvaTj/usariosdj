from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path('',views.LoginView.as_view(),name='login'),    
    path('panel/',views.HomePageView.as_view(),name='panel'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]
