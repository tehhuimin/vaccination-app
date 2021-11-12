from django.http import JsonResponse, response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
import json

from .models import *
from .serializers import * 

class GetBookingsView(APIView):
    @swagger_auto_schema(
        operation_description="Get all bookings", 
    )
    def get(self, request, format=None):
        """
        Read all bookings data
        """
        try: 
            data = Booking.objects.all()
            serializer = BookingSerializer(data, many=True)
            # TODO: serialize enum
            return JsonResponse(data = {"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetVaccineCenterView(APIView):
    @swagger_auto_schema(
        operation_description="Get list of vaccine centers", 
    )
    def get(self, request, format=None):
        """
        Get list of vaccine centers
        """
        try: 
            data = VaccinationCenter.objects.all()
            serializer = VaccinationCenterSerializer(data, many=True)
            return JsonResponse(data = {"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAvailableTimeSlots(APIView):

    @swagger_auto_schema(
        operation_description="Get available slots by filtering time_slot and center_id", 
        manual_parameters = [
            openapi.Parameter('date', openapi.IN_QUERY, description="date in YY-MM-DD format", type=openapi.TYPE_STRING), 
            openapi.Parameter('center_id', openapi.IN_QUERY, description="center_id", type=openapi.TYPE_INTEGER), 
        ]
    )
    def get(self, request):
        try: 
            selected_date = request.GET.get('date', None)
            center_id = request.GET.get('center_id', None)
            if center_id and selected_date: 
                slots_available = get_list_of_slots_available(center_id, selected_date)
                data = TimeSlotChoices.choices(slots_available)
            else:
                data = TimeSlotChoices.choices()
            return JsonResponse(data = {"success": True, "data": data}, status=status.HTTP_200_OK)
        except VaccinationCenter.DoesNotExist as e: 
            return JsonResponse({'error': str(e), 'success': False}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class NewBookingVIew(APIView): 
    @swagger_auto_schema(
        request_body=CreateBookingSerializer
    )
    def post(self, request, format=None):
        """
        Register a slot
        """
        try: 
            received_data = json.loads(request.body)
            serializer = CreateBookingSerializer(received_data)
            serialized_data = serializer.data
            user, _ = User.objects.get_or_create(
                    NRIC = serialized_data.get('NRIC', None),
                    name = serialized_data.get('name', None),
                )
            booking_created = Booking.objects.create(
                center=VaccinationCenter.objects.get(id = serialized_data.get('centerId', None)), 
                date = serialized_data.get('date', None),
                time_slot = serialized_data.get('time_slot', None), 
                NRIC = user
            )
            created_serializer = BookingSerializer(booking_created)
            return JsonResponse(data = {"success": True, "data": created_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class BookingView(APIView):
    @swagger_auto_schema(
        operation_description="Get booking by id", 
    )
    def get(self, request, uid, format=None):
        """
        Get booking by id
        """
        try: 
            booking = Booking.objects.get(id=uid)
            serializer = BookingSerializer(booking)
            return JsonResponse(data = {"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist as e:  # Throw Error 404 if data doesn't exist.  
            return JsonResponse({'error': str(e), 'success': False}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, uid, format=None):
        """
        Get list of vaccine centers
        """
        try: 
            data = json.loads(request.body)
            return JsonResponse(data = {"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, uid, format=None):
        """
        Get list of vaccine centers
        """
        try: 
            booking = Booking.objects.get(id=uid)
            booking.delete()
            return JsonResponse(data = {'success': True}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist as e: 
            return JsonResponse(data = {'error': str(e),'success': False}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)