from django.urls import path

from api.v1.hospital import views

urlpatterns = [
 path('addPatient',views.Addpatient),
 path('department',views.AllDepartments),

 path('addDep',views.AddDep),
 path('SDep/<int:id>',views.SingleDep),
 path('UDep/<int:id>',views.UpdateDep),
 path('DeleteDep/<int:id>',views.DeleteDep),
 path('bookA',views.BookAppointment),
 path('AllAppo',views.AllAppointment),
 path('AllAppoDoctor',views.AllAppointmentDoctor),
 path('SAppo/<int:id>',views.SingleAppo),
 path('UAppo/<int:id>',views.UpdateAppointment),
 path('statusU/<int:id>',views.StatusU),
 path('statusUP/<int:id>',views.StatusUP),
 path('deleteAppo/<int:id>',views.DeleteAppo),
 path('patients',views.AllPatients),
 path('Spatient/<int:id>',views.SinglePatient),
 path('deleteP/<int:id>',views.DeleteP),
 path('users/admin',views.UserA),


 path('users',views.User),
 path('users/doctor',views.UserDoctor),
 path('users/pharm',views.UserP),

 path('addPresc',views.AddPrescription),
 path('addallPresc',views.AddPrescription),
 path('viewmedicine',views.ViewMed),

 path('viewPr',views.ViewPrescription),
 path('viewPrP',views.ViewPrescriptionP),
]