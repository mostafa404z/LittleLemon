from . import views
from django.urls import path 
from . import views



urlpatterns = [
    path('login/',views.login_view,name="login"),
    path('login/create-account/',views.create_userview,name="register"),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('logout/',views.logout_view,name="logout"),
]
