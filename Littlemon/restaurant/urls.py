from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path 
from . import views

# router = DefaultRouter()
# router.register(r'tables', views.BookingViewSet)

urlpatterns = [
    path('login/',views.login,name='login'),
    path('login/create-account/',views.create_userview,name='register'),
    path('menu/',views.MenuItemsView),
    path('bookings/',views.BookingViewSet)
]
