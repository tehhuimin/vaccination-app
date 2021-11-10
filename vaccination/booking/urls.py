from django.urls import path

from .views import GetBookingsView, GetVaccineCenterView

urlpatterns = [
    path('', GetBookingsView.as_view(), name='get_bookings'),
    path('vaccine_centers', GetVaccineCenterView.as_view(), name='get_vaccine_center'),
    
    # path('<str:id>/', UsersView.as_view(), name='users')
]