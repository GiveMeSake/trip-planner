from django import forms
from .models import  Tourist


class Touristform(forms.ModelForm):
    class Meta:
        model = Tourist
        fields = ['University', 'Program', 'FirstName', 'LastName', 'Email', 'Phone', 'Password', 'Age', 'Address', 'Next_of_Kin' ]