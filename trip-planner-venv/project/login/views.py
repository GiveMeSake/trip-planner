from django.shortcuts import render
from login import models
from . import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
import json
import pprint

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
                    photo_reference = places_details['result']['photos'][3]['photo_reference']
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



def view_spot(request, spot_id):
    if 'username' not in request.session:
        return HttpResponseRedirect('/')
    username = request.session.get('username', None)
    return render(request, 'history_detail.html', {})

# Profile view
def result_page(request):
    if 'username' not in request.session:
        return HttpResponseRedirect('/')
    # fake data
    username = request.session.get('username', None)

        #from post
    destination = request.session.get('destination')
    numOfPeople = request.session.get('numOfPeople')

    if 'search_historys' not in request.session:
        request.session['search_historys'] = []
    request.session['search_historys'].append({
        'name': destination,
        'description': f'{numOfPeople} people',
        'image_url': make_curl_request("destination")
    })
    request.session.modified = True
    history = request.session.get('search_historys', [])


    #give every spot an ID
    for index, spot in enumerate(history):
        spot['id'] = index + 1
    return render(request, 'result_page.html', {'history':history,'username': username},)

def profile(request):
    # Check if username is in session. If not, redirect to root.
    if 'username' not in request.session:
        return HttpResponseRedirect('/')
    
    # Fetch user data from session
    username = request.session['username']
    userid = request.session['userid']
    user = models.UserRigister.objects.get(userid=userid)

    if request.method == 'POST':
        # If POST request, update user data and save to DB.
        updated_data = request.POST
        user.name = updated_data.get('name', user.name)
        user.gender = updated_data.get('gender', user.gender)
        user.address = updated_data.get('address', user.address)
        user.save()

        # Display success message
        messages.success(request, 'Profile updated successfully!')
    else:
        updated_data = None

    return render(request, 'profile.html', {'user': user, 'username': username, 'updated_data': updated_data})


# Login view
def login(request):
    # If already logged in, redirect to root.
    if 'username' in request.session:
        return HttpResponseRedirect('/')
    
    # If POST request, validate login data and establish session.
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            userid = request.POST['userid'].strip()
            password = request.POST['password']

            try:
                user = models.UserRigister.objects.get(userid=userid)
                if user.password == password:
                    request.session['userid'] = user.userid
                    request.session['username'] = user.name
                    return HttpResponseRedirect('/')
                else:
                    message = 'Wrong password'
            except:
                message = 'No such user'
        else:
            message = 'Please check the provided data again'
    else:
        login_form = forms.LoginForm()
    
    return render(request, 'login.html', locals())


# Logout view
def logout(request):
    # If logged in, clear all sessions and redirect to root.
    if 'username' in request.session:
        Session.objects.all().delete()
        return HttpResponseRedirect('/')


# Signup view
def signup(request):
    # If already logged in, redirect to root.
    if 'username' in request.session:
        return HttpResponseRedirect('/')
    
    # If POST request, validate and save new user data.
    if request.method == 'POST':
        signup_form = forms.SignupForm(request.POST)
        if signup_form.is_valid():
            try:
                # Check for duplicate userid
                models.UserRigister.objects.get(userid=request.POST.get('userid'))
                message = 'User ID already exists!'
            except:
                message = 'Saved successfully'
                signup_form.save()
                return HttpResponseRedirect('/login/')
        else:
            message = 'All fields are required!'
    else:
        signup_form = forms.SignupForm()

    return render(request, 'signup.html', locals())


# Index view (Home page)
def index(request):
    username = request.session.get('username', None)
    return render(request, 'index.html', {'username': username})

