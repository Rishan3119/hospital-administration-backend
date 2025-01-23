from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils.timezone import now,localtime

from web.models import Patients, Appointment, Department,CustomUser,Prescription,Medicine
from .serializers import PatientSerializer, AppointmentSerializer, DepartmentSerializer,userSerializer,PrescriptionSerializer,MedicineSerializer

# reception


# Add Patient
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Addpatient(request):
    Email=request.data['Email']
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        patient = serializer.save()
        subject = 'Patient Registration Successful'
        message = f'Your Patient ID is {patient.id}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [Email]
        send_mail(subject, message, email_from, recipient_list)
        response_data={
            "status":200,
            "message":"Patient Added Successfully"
        }
    else:
        response_data={
            "status":201,
            "message":"Data not found"
        }
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def BookAppointment(request):
    patient_id = request.data.get('patient_id')
    doctor_id = request.data.get('doctor_id')
    department_id = request.data.get('department_id')

    if patient_id and doctor_id and department_id:
        patient = Patients.objects.get(id=patient_id)
        doctor = CustomUser.objects.get(id=doctor_id, role="Doctor")
        department = Department.objects.get(id=department_id)
        today_appointments = Appointment.objects.filter(doctor=doctor, date__date=now().date())
        if today_appointments.exists():
                last_token_number = today_appointments.latest('token_number').token_number
                token_number = int(last_token_number) + 1
        else:
            token_number = 1

        subject = 'Your Appointment Details'
        message = f'Dear {patient.Name},\n\nYour appointment with Dr. {doctor.username} has been confirmed.\n' \
                      f'Token Number: {token_number}\n' \
                      f'Department: {department.department}\n\nPlease keep your token number for future reference.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [patient.Email]
        send_mail(subject, message, email_from, recipient_list)

        appointment = Appointment.objects.create(patient=patient,doctor=doctor,department=department,token_number=str(token_number))
        if appointment:
                appointment.save()
                response_data={
                    "status": 200,
                    "message": "Appointment created successfully",
                    "doctor_name": doctor.username,  
                    "token_number": appointment.token_number
                }
        else:
            response_data={
                    "status":201,
                    "message":"error"
                }
    else:
            response_data={
                "status":201,
                "message":"Please fill the Details"
                }

    return Response(response_data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UpdateAppointment(request,id):
   instance=Appointment.objects.get(id=id)
   data=request.data
   appointment=AppointmentSerializer(instance=instance,data=data,partial=True)
   if appointment.is_valid():
        appointment.save()
        response_data={
            "status":200,
            "message":"Reassigned Successfull!"
        }
   else:
       response_data={
            "status":201,
            "message":"data not found"
        }
   return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SingleAppo(request,id):
    context={
        "request":request
    }
    if Appointment.objects.get(id=id):
      appointment=Appointment.objects.get(id=id)
      serializer=AppointmentSerializer(instance=appointment,context=context)
      if serializer:
            response_data={
                "status":200,
                "data":serializer.data
            }
      else:
            response_data={
                "status":201,
                "message":"data not found"
            }  
    else:
        response_data={
                "status":201,
                "message":f"student with id {id} does not exist"
            }  
    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def AllDepartments(request):
    department=request.GET.get('department')
    context={
        "request":request
    }
    if department:
        departments = Department.objects.filter(department__icontains=department)
    else:
        departments = Department.objects.all()  
    serializer = DepartmentSerializer(instance=departments, many=True,context=context)
    if serializer:
        response_data = {
        "status": 200,
        "data": serializer.data
        }
    else:
            response_data = {
            "Status": 201,
            "message": "data not found",
            }
    return Response(response_data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddDep(request):
   data=request.data
   user=request.user.id
   data['user']=user
   department=DepartmentSerializer(data=data)
   if department.is_valid():
        department.save()
        response_data={
            "status":200,
            "message":"department Added Successfully"
        }
   else:
       response_data={
            "Status":201,
            "message":"data not Added"
        }
   return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SingleDep(request,id):
    context={
        "request":request
    }
    if Department.objects.get(id=id):
      book=Department.objects.get(id=id)
      serializer=DepartmentSerializer(instance=book,context=context)
      if serializer:
            response_data={
                "status":200,
                "data":serializer.data
            }
      else:
            response_data={
                "status":201,
                "message":"data not found"
            }  
    else:
        response_data={
                "status":201,
                "message":f"student with id {id} does not exist"
            }  
    return Response(response_data)

@api_view(['PUT'])
@permission_classes([AllowAny])
def UpdateDep(request,id):
   instance=Department.objects.get(id=id)
   data=request.data
   if data['image']=="":
       data=request.data.copy()
       data['image']=instance.image
       
   department=DepartmentSerializer(instance=instance,data=data,partial=True)
   if department.is_valid():
        department.save()
        response_data={
            "status":200,
            "message":"Updated Successfully"
        }
   else:
       response_data={
            "status":201,
            "message":"data not found"
        }
   return Response(response_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteDep(request,id):
   department=Department.objects.get(id=id)
   if department:
        department.delete()
        response_data={
            "status":200,
            "message":"success"
        }
   else:
       response_data={
            "status":201,
            "message":"data not found"
        }
   return Response(response_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteP(request,id):
   patient=Patients.objects.get(id=id)
   if patient:
        patient.delete()
        response_data={
            "status":200,
            "message":"success"
        }
   else:
       response_data={
            "status":201,
            "message":"data not found"
        }
   return Response(response_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteAppo(request,id):
   appointment=Appointment.objects.get(id=id)
   if appointment:
        appointment.delete()
        response_data={
            "status":200,
            "message":"success"
        }
   else:
       response_data={
            "status":201,
            "message":"data not found"
        }
   return Response(response_data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AllPatients(request):
    patient_id = request.GET.get('patient_id')
    context={
        "request":request
    }
    if patient_id:
        patients = Patients.objects.filter(id=patient_id)
    else:
        patients = Patients.objects.all()  
    serializer = PatientSerializer(instance=patients, many=True,context=context)
    if serializer:
        response_data = {
        "status": 200,
        "data": serializer.data
        }
    else:
            response_data = {
            "Status": 201,
            "message": "data not found",
            }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AllAppointment(request):
    appointment_id = request.GET.get('appointment_id')
    patient_id = request.GET.get('patient_id')
    context={
        "request":request
    }
    if appointment_id:
        appointments = Appointment.objects.filter(id=appointment_id)
    elif patient_id:
        
        appointments = Appointment.objects.filter(patient_id=patient_id)
    else:
        appointments = Appointment.objects.all()  
    serializer = AppointmentSerializer(instance=appointments, many=True,context=context)
    if serializer:
        response_data = {
        "status": 200,
        "data": serializer.data
        }
    else:
            response_data = {
            "Status": 201,
            "message": "data not found",
            }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AllAppointmentDoctor(request):
    user = request.user
    if user.role != "Doctor":
        return Response({
            "status": 403,
            "message": "Unauthorized. Only doctors can access this."
        })
    
    appointment_id = request.GET.get('appointment_id')
    patient_id = request.GET.get('patient_id')

    context = {
        "request": request
    }
    
    if appointment_id:
        
        appointments = Appointment.objects.filter(id=appointment_id, doctor=user)
    elif patient_id:
        
        appointments = Appointment.objects.filter(patient_id=patient_id, doctor=user)
    else:
        
        appointments = Appointment.objects.filter(doctor=user)

    
    serializer = AppointmentSerializer(instance=appointments, many=True, context=context)
    
    if serializer.data:
        response_data = {
            "status": 200,
            "data": serializer.data
        }
    else:
        response_data = {
            "status": 201,
            "message": "Data not found",
        }

    return Response(response_data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def StatusU(request,id):
    instance=Appointment.objects.get(id=id)

    status=AppointmentSerializer(instance,data={'is_status':True},partial=True)
    if status.is_valid():
        status.save()
        response_data={
            "status":200,
            "message":'success'
        }
    else:
        response_data={
            "status":201,
            "message":"error"
        }
    return Response(response_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def StatusUP(request,id):
    instance=Prescription.objects.get(id=id)

    status=PrescriptionSerializer(instance,data={'is_status':True},partial=True)
    if status.is_valid():
        status.save()
        response_data={
            "status":200,
            "message":'success'
        }
    else:
        response_data={
            "status":201,
            "message":"error"
        }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def User(request):
    department_id = request.GET.get('department_id')
    
    if department_id:
        user = CustomUser.objects.filter(role="Doctor", dep_id=department_id)  # Adjust field name as needed
    else:
        user = CustomUser.objects.filter(role="Doctor")
    
    serializer = userSerializer(instance=user, many=True, context={"request": request})
    
    if serializer.data:
        response_data = {
            "status": 200,
            "data": serializer.data
        }
    else:
        response_data = {
            "status": 201,
            "message": "data not found"
        }
    
    return Response(response_data)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserDoctor(request):
    user=CustomUser.objects.filter(id=request.user.id,role="Doctor")
    print(user)
    context={
        "request":request 
    }
    serializer=userSerializer(instance=user,many=True,context=context)
    if serializer:
        response_data={
            "status":200,
            "data":serializer.data
        }
    else:
        response_data={
            "status":201,
            "message":"data not found"
        }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserP(request):
    user=CustomUser.objects.filter(id=request.user.id,role="Pharmacist")
    print(user)
    context={
        "request":request 
    }
    serializer=userSerializer(instance=user,many=True,context=context)
    if serializer:
        response_data={
            "status":200,
            "data":serializer.data
        }
    else:
        response_data={
            "status":201,
            "message":"data not found"
        }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserA(request):
    user=CustomUser.objects.filter(id=request.user.id)
    print(user)
    context={
        "request":request 
    }
    serializer=userSerializer(instance=user,many=True,context=context)
    if serializer:
        response_data={
            "status":200,
            "data":serializer.data
        }
    else:
        response_data={
            "status":201,
            "message":"data not found"
        }
    return Response(response_data)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddPrescription(request):
    data = request.data
    appointment_id = data.get('appointment_id')
    doctor_id = data.get('doctor_id')
    patient_id = data.get('patient_id')
    department_id = data.get('department_id')
    medicine= data.get('medicine')
    
    

    if not all([appointment_id, doctor_id, patient_id, department_id]):
        return Response({
            "status": 400,
            "message": "Missing required fields."
        })

    appointment = Appointment.objects.filter(id=appointment_id).first()
    doctor = CustomUser.objects.filter(id=doctor_id).first()
    patient = Patients.objects.filter(id=patient_id).first()
    department = Department.objects.filter(id=department_id).first()
   

    if not appointment or not doctor or not patient or not department:
        return Response({
            "status": 400,
            "message": "Invalid appointment, doctor, patient, or department information."
        })

    prescription= Prescription.objects.create(appointment=appointment,patient=patient,
                doctor=doctor,dep=department)
    prescription.save()
    for item in medicine:
        print(medicine)
        medicine=Medicine.objects.create(prescription=prescription,medicine_name=item['medicineName'],
                                         consumption_time=item['consumptionTime'])
        
    response_data={
        "status":200,
        "message":"success"
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def ViewMed(request):
    medicines = Medicine.objects.all()  
    serializer = MedicineSerializer(instance=medicines, many=True)
    if serializer:
        response_data = {
        "status": 200,
        "data": serializer.data
        }
    else:
            response_data = {
            "Status": 201,
            "message": "data not found",
            }
    return Response(response_data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ViewPrescription(request):
    prescription_id = request.GET.get('prescription_id')
    patient_id = request.GET.get('patient_id')
    department_id = request.GET.get('department_id')  
    
    context = {
        "request": request
    }

    if prescription_id:
        prescriptions = Prescription.objects.filter(id=prescription_id)
    elif patient_id:
        prescriptions = Prescription.objects.filter(patient_id=patient_id)
    elif department_id:
        prescriptions = Prescription.objects.filter(department_id=department_id)  # Filter by department_id
    else:
        prescriptions = Prescription.objects.all()

    serializer = PrescriptionSerializer(instance=prescriptions, many=True, context=context)
    
    if prescriptions.exists():
        response_data = {
            "status": 200,
            "data": serializer.data
        }
    else:
        response_data = {
            "status": 404,
            "message": "No data found"
        }
    
    return Response(response_data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ViewPrescriptionP(request):
    prescription_id = request.GET.get('prescription_id')
    patient_id = request.GET.get('patient_id')
    department_id = request.GET.get('department_id')  # Capture department_id from the request

    context = {
        "request": request
    }
    
    if prescription_id:
        # Filter by specific prescription ID
        prescriptions = Prescription.objects.filter(id=prescription_id)
    elif patient_id:
        # Filter by patient ID
        prescriptions = Prescription.objects.filter(patient_id=patient_id)
    elif department_id:
        # Filter by department ID
        prescriptions = Prescription.objects.filter(department_id=department_id)
    else:
        # If no filters are provided, return all prescriptions
        prescriptions = Prescription.objects.all()

    serializer = PrescriptionSerializer(instance=prescriptions, many=True, context=context)
    
    if serializer.data:
        response_data = {
            "status": 200,
            "data": serializer.data
        }
    else:
        response_data = {
            "status": 404,
            "message": "Data not found",
        }

    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SinglePatient(request,id):
    context={
        "request":request
    }
    if Patients.objects.get(id=id):
      book=Patients.objects.get(id=id)
      serializer=PatientSerializer(instance=book,context=context)
      if serializer:
            response_data={
                "status":200,
                "data":serializer.data
            }
      else:
            response_data={
                "status":201,
                "message":"data not found"
            }  
    else:
        response_data={
                "status":201,
                "message":f"patient with id {id} does not exist"
            }  
    return Response(response_data)






