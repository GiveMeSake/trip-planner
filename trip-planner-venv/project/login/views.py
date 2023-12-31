from django.shortcuts import render
from login import models
from . import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Profile view
def result_page(request):
    
    # fake data
    username = request.session.get('username', None)
    recommended_spots = [
        {
            'name': 'Sunset Beach',
            'description': 'A beautiful beach known for its stunning sunsets.',
            'image_url': 'https://images.pexels.com/photos/3106799/pexels-photo-3106799.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
        },
        {
            'name': 'Mountain Peak',
            'description': 'A challenging but rewarding mountain hike with breathtaking views.',
            'image_url': 'https://as1.ftcdn.net/v2/jpg/05/65/76/92/1000_F_565769257_yaHRp8Pts9SjlnSzHKNrQs264KoIsiwE.jpg'
        },
        {
            'name': 'Historic Old Town',
            'description': 'Explore the rich history of the old town, with its classic architecture and charming streets.',
            'image_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a5/King_Street_restaurants.jpg'
        }
  
    ]


    return render(request, 'result_page.html', {'recommended_spots': recommended_spots,'username': username},)

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

