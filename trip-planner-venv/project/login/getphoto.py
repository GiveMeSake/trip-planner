import requests
import json
import pprint
from django.http import HttpResponse


def make_curl_request(location):
    # API Key
    api_key = "AIzaSyAh_xUoUaAUmGZyyGdXcmt13Kzk8rukyL4"

    # Google Places API endpoint for place id
    url_place_id = "https://places.googleapis.com/v1/places:searchText"

    # Your curl-like parameters
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress',
    }

    data = {
        'textQuery': location
    }
    response = requests.post(url_place_id, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        # Successful request, you can now handle the response data
        places_data = response.json()
        # Process 'places_data' as needed
        if (places_data['places'][0]['id']):
            place_id = places_data['places'][0]['id']
            print(place_id)
            # Google Places API endpoint for place details
            url_place_details = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'
            response = requests.post(url_place_details, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                places_details = response.json()
                # print(places_details)
                pprint.pprint(places_details)
                if "photos" in places_details['result']:
                    photo_reference = places_details['result']['photos'][0]['photo_reference']
                    print(photo_reference)
                    print('-----------------FINAL URL----------------')
                    print(f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=600&maxheight=400&photoreference={photo_reference}&key={api_key}")
                else:
                    # Handle the error
                    print(f"Error: Place photos not found")
                    # TODOadd a default picture
            else:
                # Handle the error
                print(f"Error: Place ID not found")
        else:  
            # Handle the error
            print(f"Error: Place ID not found")
    else:
        # Handle the error
        print(f"Error: {response.status_code} - {response.text}")

# Function call
make_curl_request("White House")
