from django.shortcuts import render, redirect
from .models import Tourist
from .forms import Touristform
from django.contrib import messages



# Create your views here.
def home(request):
    all_Tourists = Tourist.objects.all()
    return render(request, 'home.html', {'all' :all_Tourists})

def join(request):
    if request.method == "POST":
        form = Touristform(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            University = request.POST['University']
            Program = request.POST['Program']
            FirstName = request.POST['FirstName']
            LastName = request.POST['LastName']
            Email = request.POST['Email']
            Phone = request.POST['Phone']
            Password = request.POST['Password']
            Age = request.POST['Age']
            Address = request.POST['Address']
            Next_of_Kin = request.POST['Next_of_Kin']
            messages.error(request, 'There are errors in the form. Please review and correct the information.')
            return render(request, 'join.html', {'University' :University,
                                                'Program' :Program,
                                                'FirstName' :FirstName,
                                                'LastName' :LastName,
                                                'Email' :Email,
                                                'Phone' : Phone,
                                                'Password' :Password,
                                                'Age' :Age,
                                                'Address' :Address,
                                                'Next_of_Kin' :Next_of_Kin,
                                                })
        
        
            messages.success(request, ('Yeyyy...Submission Success! '))
        #return render(request, 'home.html', {})
        return redirect('home')

    else: 
        return render(request, 'join.html', {})

#def add_post(request):
    # Your view logic here
