from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Employee
# for authentication we have to import authentication used in login page
from django.contrib.auth import authenticate

# Create your views here.

def home(req):
    return render(req, 'home.html')

def register(req):
    return render(req, 'register.html')

def login(req):
    return render(req, 'login.html')

def user(req):
    return render(req,'user.html')

# def aadmin(req):
#     return render(req,'admin.html')

def employee(req):
    return render(req,'employee.html')

def signup(req):
    # storing data into database
    if req.method=='POST':
        name=req.POST.get('name')
        email=req.POST.get('email')
        password=req.POST.get('password')
        confirmpassword=req.POST.get('confirmpassword')

        # if email already exist
        if User.objects.filter(Email=email).exists():
            return render(req,'register.html', {'Emailmsg':'email already exist'})
        
        # check pass == cpass
        if password==confirmpassword:
            User.objects.create(Name=name, Email=email, Password=password, ConfirmPassword=confirmpassword).save()
            return redirect('index')
        
        else:
            return render(req,'register.html',{'Passmsg':'password do not match'})    

def signin(req):
    if req.method=='POST':
        email=req.POST.get('email')
        password=req.POST.get('password')
        # using filter function
        #1-->for NewUser check
        Newuser=User.objects.filter(Email=email, Password=password).first()
        if Newuser is not None:
            return redirect('user')
        
        #2--> for admin (use 'and' instead of &) check
        if email=='admin@gmail.com' and password=='admin@123':
             return redirect('aadmin')
        
        else:
            return render(req,'login.html',{'Newusermsg':'Invalid email or password'})

    # 3->for employee
    else:
        pass     



# ----------------------------------------admin-interface---------------------------------

def aadmin(req):
    return render(req,'admin.html')

def register_emp(req):
     return render(req, 'register_emp.html')

def add_emp(req):
     if req.method=='POST':
        emp_name=req.POST.get('emp_name')
        emp_email=req.POST.get('emp_email')
        emp_username=req.POST.get('emp_username')
        emp_password=req.POST.get('emp_password')

        # if email already exist 
        if Employee.objects.filter(Emp_email=emp_email).exists():
            return render(req,'register_emp.html', {'EmpEmailmsg':'email already exist'})
        
        if Employee.objects.filter(Emp_username=emp_username).exists():
            return render(req,'register_emp.html', {'EmpUsernamemsg':'username already exist'})
        
        else:
            Employee.objects.create(
                Emp_name=emp_name,
                Emp_email=emp_email, 
                Emp_username=emp_username,
                Emp_password=emp_password).save()
            return render('aadmin')
        


#  logout code    
def logout(req):
    return render(req,'home.html')    
        
