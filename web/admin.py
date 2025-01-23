from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from web.models import CustomUser,Patients,Department,Appointment,Prescription,Medicine

# Register your models here.
class CustomAdmin(UserAdmin):
    list_display=['id','username','email','last_name','phone','image','is_active','role','dep']
admin.site.register(CustomUser,CustomAdmin)


class PatientAdmin(admin.ModelAdmin):
    list_display=['id','Name','Email','Phone','Gender','Address']
admin.site.register(Patients,PatientAdmin)

class MedicineAdmin(admin.ModelAdmin):
    list_display=['id','medicine_name','consumption_time','prescription']
admin.site.register(Medicine,MedicineAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display=['id','department','image','desc']
admin.site.register(Department,DepartmentAdmin)

class PrescriptionAdmin(admin.ModelAdmin):
    list_display=['id','doctor','patient','appointment','date','dep','is_status']
admin.site.register(Prescription,PrescriptionAdmin)


class appointmentAdmin(admin.ModelAdmin):
    list_display=['id','doctor','patient','department','token_number','date','is_status']
admin.site.register(Appointment,appointmentAdmin)