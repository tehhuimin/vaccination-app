from django.urls import path

from .views import GetBookingsView

urlpatterns = [
    path('', GetBookingsView.as_view(), name='get_bookings'),
    # path('<str:id>/', UsersView.as_view(), name='users')
]