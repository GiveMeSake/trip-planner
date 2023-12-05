from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.conf import settings
import openai
import re
import json
import pprint
import requests
def make_curl_request(location):
    # API Key
    api_key = settings.GOOGLE_API_KEY

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
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=600&maxheight=400&photoreference={photo_reference}&key={api_key}"
                    return photo_url
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
        
def input_validation(request):
    validationText = request.POST.get('validationText', '')
    
    openai.api_key = settings.OPENAI_API_KEY

    print(validationText)
    completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": validationText}
        ]
    )

    is_valid = completion.choices[0].message.content

    return JsonResponse({'isValid': is_valid})

def show_results(request):
    if request.method == 'POST':
        # Parse the JSON data from the request
        final_prompt = request.POST.get('finalPrompt', '')
    
        openai.api_key = settings.OPENAI_API_KEY

        match = re.search(r'to\s+(.*?)\s+for', final_prompt)
        if match:
            destination = match.group(1).strip()
        match = re.search(r'for\s+(\d+)\s+people', final_prompt)
        if match:
            numOfPeople = match.group(1).strip()
        match = re.search(r'of\s+(\d+)\s+for', final_prompt)
        if match:
            budget = match.group(1).strip()
        match = re.search(r'for\s+(\d+)\s+days', final_prompt)
        if match:
            days = match.group(1).strip()

        request.session['destination'] = destination
        request.session['numOfPeople'] = numOfPeople
        request.session['budget'] = budget
        request.session['days'] = days

        completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
            messages=[
                {"role":"assistant", "content": final_prompt}
            ]
        )
        
        final_result = completion.choices[0].message.content
        history = request.session.get('search_historys', [])
        spot_id = len(history) + 1

        # Append new spot data to history
        new_spot = {
            'id': spot_id,
            'name': destination,
            'days': days,
            'budget': budget,
            'final_result': final_result,
            'image_url': make_curl_request(destination),
            'description': f'{numOfPeople} people',
        }
        history.append(new_spot)
        request.session['search_historys'] = history
        request.session.modified = True

        # Redirect to the view_spot URL with the new spot ID
        return redirect(f'/view_spot/{spot_id}/')

    else:
        # Handle non-POST requests if necessary
        return JsonResponse({'error': 'Invalid request'}, status=400)