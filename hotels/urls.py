# hotels/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_booking_page, name='hotel_booking_page'),
    path('api/hotels/', views.search_hotels, name='search_hotels'),  # API endpoint for hotels
]
