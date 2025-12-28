from django.db import models

# Create your models here.

#----------------------table for new user----------------------------

class User(models.Model):
    Name=models.CharField(max_length=20)
    Email=models.EmailField()
    Password=models.CharField(max_length=128)
    ConfirmPassword=models.CharField(max_length=128)    

#---------------------table for employee----------------------------

class Employee(models.Model):
    Emp_name=models.CharField(max_length=40)
    Emp_email=models.EmailField()
    Emp_username=models.CharField(max_length=100)
    Emp_password=models.CharField(max_length=128)