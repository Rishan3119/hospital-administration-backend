from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
gender=(
    ('',''),
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
)

Day=(
    ('Morning','Morning'),
    ('Afternoon','afternoon'),
    ('Evening','Evening'),
    ('Night','night'),
    ('Morning,Afternoon,Night','Morning,Afternoon,Night'),
    ('Morning','Night'),
)
class Department(models.Model):
    department= models.CharField(max_length=100)
    image=models.ImageField(upload_to='dep_image',blank=True,null=True)
    desc=models.TextField(default="")

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Doctor', 'Doctor'),
        ('Pharmacist', 'Pharmacist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone=models.DecimalField(decimal_places=0,max_digits=10,null=True)
    image=models.ImageField(upload_to='user_image',blank=True,null=True)
    dep = models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True) 

class Patients(models.Model):
    Name=models.CharField(max_length=20,default="")
    Email=models.EmailField()
    Address=models.TextField()
    Phone=models.DecimalField(decimal_places=0,max_digits=10,null=True)
    Gender=models.CharField(choices=gender,max_length=10)
    

class Appointment(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE,default="")
    doctor = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default="")
    department = models.ForeignKey(Department, on_delete=models.CASCADE,default="")
    token_number = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    is_status=models.BooleanField(default=False)

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    dep = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_status = models.BooleanField(default=False)

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=255)
    consumption_time = models.CharField(max_length=255) 
    prescription  = models.ForeignKey(Prescription,on_delete=models.CASCADE,null=True,blank=True)



