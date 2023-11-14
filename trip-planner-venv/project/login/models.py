from django.db import models
from django.core.validators import validate_comma_separated_integer_list

# Create your models here.

class UserRigister(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    userid = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=20, null=False)
    email = models.EmailField()
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Male')
    address = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name
