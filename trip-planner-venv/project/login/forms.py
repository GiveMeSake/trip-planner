from django import forms
from .import models
from captcha.fields import CaptchaField
class DateInput(forms.DateInput):
	input_type = 'date'

class SignupForm(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = models.UserRigister
		fields =  ['userid', 'password','email','name' ]
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		
		self.fields['userid'].label 	= 'set ID'
		self.fields['password'].label 	= 'set passwprd'
		self.fields['email'].label 	= 'email'
		self.fields['name'].label 	= 'your username'
		self.fields['captcha'].label 	='pleas insert'

class LoginForm(forms.Form):
	userid = forms.CharField(label = 'id', max_length=20)
	password = forms.CharField(label = 'password',widget = forms.PasswordInput())

	
