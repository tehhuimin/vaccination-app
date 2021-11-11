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

class NewBookingVIew(APIView): 
    def post(self, request, format=None):
        """
        Register a slot
        """
        try: 
            data = json.loads(request.body)
            return JsonResponse(data = {"success": True, "data": data}, status=status.HTTP_200_OK)
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
            return JsonResponse({'error': e,'success': False}, status=status.HTTP_404_NOT_FOUND) 
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)