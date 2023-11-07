from django.contrib import admin
from login import models
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display =('id','name','userid','password','email','gender')
	ording=('-pub_time',)
 
admin.site.register(models.UserRigister, UserAdmin)