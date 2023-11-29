from django.db import models

# Create your models here. define the columns in tables 

class Tourist(models.Model):
    University = models.CharField(max_length=50)
    Program = models.CharField(max_length=50)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Phone = models.IntegerField()
    Password = models.CharField(max_length=50)
    Age = models.IntegerField()
    Address = models.CharField(max_length=100)
    Next_of_Kin = models.CharField(max_length=50)
    
    def __str__(self):
        return self.University +  '  : ' + self.FirstName +   '  : ' + self.LastName +  '  : ' + self.Email  
    
    
