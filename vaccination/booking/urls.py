from django.urls import path

from .views import GetBookingsView, GetVaccineCenterView, BookingView, NewBookingVIew

urlpatterns = [
    path('', GetBookingsView.as_view(), name='get_bookings'),
    path('vaccine_centers', GetVaccineCenterView.as_view(), name='get_vaccine_center'),
    path('<str:uid>/', BookingView.as_view(), name='get_booking'), 
    path('add', NewBookingVIew.as_view(), name="create_booking")
]