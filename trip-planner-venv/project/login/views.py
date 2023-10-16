from django.shortcuts import render
from login import models
from . import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
def profile(request):
	if 'username' in request.session==None:
		return HttpResponseRedirect('/')
	username=request.session['username']
	userid=request.session['userid']
	user = models.UserRigister.objects.get(userid = userid)
	profile_form=forms.ProfileForm()
	if request.method =='POST':
		profile_form = forms.ProfileForm(request.POST)
		if profile_form.is_valid():
			message = 'Saved successfully'


			username=user.name
			request.session['username']=user.name
		else:
			message = 'Fields are required!!'
	else:
		profile_form = forms.ProfileForm()
		message = 'Fields are required!!'


	return render(request,'profile.html',locals())

def login(request):
	if 'username' in request.session:
		username=request.session['username']
		return HttpResponseRedirect('/')
	if request.method =='POST':
		login_form = forms.LoginForm(request.POST)
		if login_form.is_valid():
			userid = request.POST['userid'].strip()
			password = request.POST['password']
			try:
				user = models.UserRigister.objects.get(userid = userid)
				if user.password == password:
					request.session['userid']=user.userid
					request.session['username']=user.name
					return HttpResponseRedirect('/')
				else:
					message = 'wrong password'
			except:
				message = 'no user'
		else:
			message='pleasw check it again'
	else:
		login_form = forms.LoginForm()
	return render(request,'login.html',locals())

# def signin(request):
#     return render(request, 'psignin.html',locals())

def logout(request):
	if 'username' in request.session:
		Session.objects.all().delete()
		return HttpResponseRedirect('/')

def signup(request):

	signup_form=forms.SignupForm()
	if 'username' in request.session:
		username=request.session['username']
		return HttpResponseRedirect('/')

	if request.method =='POST':
		signup_form = forms.SignupForm(request.POST)
		if signup_form.is_valid():
			try: 
				models.UserRigister.objects.get(userid=request.POST.get('userid'))
				message = 'userid repeat'
				
			except:
				message = 'Saved successfully'
				signup_form.save()
				return HttpResponseRedirect('/')
		else:
			message = 'Fields are required!!'
	else:
		signup_form = forms.SignupForm()
	


	return render(request, 'signup.html',locals())

def index(request):
    username = request.session.get('username', None)
    return render(request, 'index.html', {'username': username})
