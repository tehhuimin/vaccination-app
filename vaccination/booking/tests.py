from django.test import TestCase, Client
from .models import * 
from django.urls import reverse
import json    

class MyTest(TestCase):
    
    fixtures = ['data.json']

    def test_get_all_bookings(self): 
        """
            Test Case: GET /bookings
            Test if API is able to retrieve a list of all bookings
        """
        response = self.client.get(reverse('get_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('data' in response.json())
        response_data = response.json()
        self.assertTrue('success' in response_data)
        self.assertTrue('data' in response_data)
        response_data = response_data['data']

        self.assertEqual(len(response_data), 5)

        # check booking data is correct
        data1 = response_data[0]
        db_data1 = Booking.objects.get(id=data1.get('id'))
        self.assertEqual(data1.get('id'), db_data1.id )
        self.assertEqual(data1.get('name'), db_data1.NRIC.name )
        self.assertEqual(data1.get('NRIC'), db_data1.NRIC.NRIC )
        self.assertEqual(data1.get('centerName'), db_data1.center.name )
        self.assertEqual(data1.get('centerId'), db_data1.center.id )
        self.assertEqual(data1.get('startTime'), db_data1.date.strftime("%Y-%m-%d") )
        self.assertEqual(data1.get('timeSlot'), db_data1.time_slot )

    def test_get_booking(self): 
        """
            Test Case: GET /bookings/<str:uid>/
            Test if API is able to retrieve data of a specific booking based on the booking id
        """
        booking_id = '2'
        response = self.client.get(reverse('get_booking', args=[booking_id]))

        # check response format
        self.assertEqual(response.status_code, 200)
        self.assertTrue('data' in response.json())
        response_data = response.json()
        self.assertTrue('success' in response_data)
        self.assertTrue('data' in response_data)
        response_data = response_data['data']

        # check booking data is correct
        data1 = response_data
        db_data1 = Booking.objects.get(id=data1.get('id'))
        self.assertEqual(data1.get('id'), db_data1.id )
        self.assertEqual(data1.get('name'), db_data1.NRIC.name )
        self.assertEqual(data1.get('NRIC'), db_data1.NRIC.NRIC )
        self.assertEqual(data1.get('centerName'), db_data1.center.name )
        self.assertEqual(data1.get('centerId'), db_data1.center.id )
        self.assertEqual(data1.get('startTime'), db_data1.date.strftime("%Y-%m-%d") )
        self.assertEqual(data1.get('timeSlot'), db_data1.time_slot )
    
    def test_get_booking_not_found(self): 
        """
            Test Case: GET /bookings/<str:uid>/
            Test if API is able to return 404 if a specific booking is not found
        """
        booking_id = '20'
        response = self.client.get(reverse('get_booking', args=[booking_id]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue('error' in response.json())
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], 'Booking matching query does not exist.')

    def tests_delete_booking(self):
        """
            Test Case: DELETE /bookings/<str:id>/
            Test if API is able to delete user given the user's id
        """
        booking_id = '2'
        response = self.client.delete(reverse('get_booking', args=[booking_id]))

        # check response format
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in response.json())
        response_data = response.json()
        self.assertTrue(response_data['success'])
        
        # check if booking has already been deleted
        response = self.client.get(reverse('get_booking', args=[booking_id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue('error' in response.json())
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], 'Booking matching query does not exist.')
    
    def tests_delete_booking_id_not_found(self):
        """
            Test Case: DELETE /bookings/<str:id>/
            Test if API is able to return 404 is booking id not found
        """
        booking_id = '200'
        response = self.client.delete(reverse('get_booking', args=[booking_id]))

        # check response format
        self.assertEqual(response.status_code, 404)
        self.assertTrue('error' in response.json())
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], 'Booking matching query does not exist.')
    





        
 



    




