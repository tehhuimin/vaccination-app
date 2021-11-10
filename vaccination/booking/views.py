from django.http import JsonResponse, response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

class GetBookingsView(APIView):
    @swagger_auto_schema(
        operation_description="Get all bookings", 
    )
    def get(self, request, format=None):
        """
        Read all bookings data
        """
        try: 
            data = [
                {
                    "id": 1,
                    "name": "Tan Ah Kow",
                    "centerName": "Bukit Timah CC",
                    "centerId": 3,
                    "startTime": "2021-12-01T09:00:00",
                },
                {
                    "id": 2,
                    "name": "Jean Lee Ah Meow",
                    "centerName": "Bukit Timah CC",
                    "centerId": 3,
                    "startTime": "2021-12-01T10:00:00",
                },
                {
                    "id": 3,
                    "name": "Lew Ah Boi",
                    "centerName": "Bukit Timah CC",
                    "centerId": 3,
                    "startTime": "2021-12-01T11:00:00",
                },
            ]
            return JsonResponse(data = {"success": True, "data": data}, status=status.HTTP_200_OK)
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
            data = [
                { "name": "None", "id": 0},
                { "name": "Bukit Batok CC", "id": 1 },
                { "name": "Bukit Panjang CC", "id": 2 },
                { "name": "Bukit Timah CC", "id": 3 },
                { "name": "Outram Park Polyclinic", "id": 4 },
            ]
            return JsonResponse(data = {"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookingView(APIView):
    @swagger_auto_schema(
        operation_description="Get booking by id", 
    )
    def get(self, request, uid, format=None):
        """
        Get list of vaccine centers
        """
        try: 
            data = {
                "id": uid,
                "name": "Tan Ah Kow",
                "centerName": "Bukit Timah CC",
                "centerId": 3,
                "startTime": "2021-12-01T09:00:00",
            }
            return JsonResponse(data = {"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, uid, format=None):
        """
        Get list of vaccine centers
        """
        try: 
            data = {
                "id": uid,
                "name": "Tan Ah Kow",
                "centerName": "Bukit Timah CC",
                "centerId": 3,
                "startTime": "2021-12-01T09:00:00",
            }
            print("delete", uid)
            return JsonResponse(data = {"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e: 
            return JsonResponse(data={'error': str(e), 'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)