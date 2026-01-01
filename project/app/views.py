from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Employee
import random  # use random to generate otp
from django.core.mail import send_mail  # for email

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
        
        # check fields are empty or not
        if not name:
            return render(req, 'register.html', {'name_error': 'Name is required'})
        if not email:
            return render(req, 'register.html', {'email_error': 'Email is required'})
        if not password:
            return render(req, 'register.html', {'Passmsg': 'Password is required'})
        if not confirmpassword:
            return render(req, 'register.html', {'Passmsg': 'Confirm password is required'})

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

#--------------------------------------------forget pass----------------------------------
def forget_pass(req):
    return render(req,'forget_pass.html')

def reset_pass(req):
    if req.method=='POST':
        email=req.POST.get('email')
       
        # email check(validation)
        if not email:
            return render(req,'forget_pass.html', {'resetEmailmsg':'Please enter email'})
        
        if not User.objects.filter(Email=email).exists():  
            return render(req,'forget_pass.html', {'resetEmailmsg':'This email is not registered!'})

        otp=random.randint(1111,9999)   # generate otp by using random module
        req.session['email'], req.session['otp']= email, otp   #using session to check otp is valid or not:
        # print(email, otp)
        
        send_mail('OTP Corporate Management System',
                  f'generate OTP for Corporate Management System is {otp}',
                  #from@gmail.com
                  'guptavaishali628@gmail.com',
                  #to@gmail.com
                  [email],
                  fail_silently=False,
        )

        return render(req,'reset.html')
        

def reset(req):
    if req.method=='POST':
        n_otp=req.POST.get('v_otp')
        n_pass=req.POST.get('new_pass')
        c_pass=req.POST.get('c_pass')

        email=req.session['email']
        otp=req.session['otp']
        
        if not n_otp:   #check otp is empty or not
            return render(req,'reset.html',{'invalidOTPmsg':'Please enter OTP'})
        
        if str(n_otp) != str(otp):  # check new otp==otp
            return render(req,'reset.html',{'invalidOTPmsg':'Invalid OTP'})

        if n_pass == c_pass:
            newUserdata=User.objects.filter(Email=email)
            # check user exit or not
            if newUserdata.exists():
                newUserdata=newUserdata.first()
                # print(newUserdata.Password)
                newUserdata.Password=n_pass
                newUserdata.save()
                # clear session
                del req.session['email']
                del req.session['otp']
                return render(req, 'login.html', {'successResetmsg':'Password reset Successfully'})
            else:
                return render(req,'reset.html',{'userExitmsg':'User not found'})
        else:
            return render(req,'reset.html', {'passMatchmsg':'password do not match'}) 


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
        
