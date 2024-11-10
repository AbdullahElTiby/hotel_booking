# hotels/views.py
import requests
from django.shortcuts import render
from django.http import JsonResponse

def get_amadeus_token():
    """Retrieve access token from Amadeus API"""
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'GFdwyQ7GyKwMR8X1syM5FHdtK8qtO7hs',  # Replace with your Amadeus API key
        'client_secret': '9DvbG6bzkKB5xlo8'  # Replace with your Amadeus API secret
    }

    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to retrieve access token")
    
def hotel_booking_page(request):
    """Render the hotel booking page"""
    return render(request, 'hotel_booking.html')    
    
def search_hotels(request):
    """Search for hotels using Amadeus API"""
    try:
        access_token = get_amadeus_token()
        city_code = request.GET.get('city', 'IST')  # Default to Istanbul (IST)
        check_in_date = request.GET.get('check_in', '2024-11-20')
        check_out_date = request.GET.get('check_out', '2024-11-25')

        # Correct Amadeus API URL for hotel search by city
        url = f"https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city?cityCode={city_code}"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Make the API request
        response = requests.get(url, headers=headers)
        data = response.json()

        print("Amadeus API Response:", response.status_code, data)  # Log the full response

        if response.status_code == 200:
            # Safely check if the 'data' exists and is a list
            hotels = data.get('data', [])
            if isinstance(hotels, list) and hotels:
                return JsonResponse({"hotels": hotels})
            else:
                return JsonResponse({"error": "No hotels found or unexpected data format"}, status=404)
        else:
            return JsonResponse({"error": "Failed to fetch hotels", "details": data}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




    
