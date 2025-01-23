from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated

from django.core.mail import send_mail
from django.conf import settings

import random

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from web.models import CustomUser,Department
from .serializers import userSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def Signup(request):
   email=request.data['email']
   username=request.data['username']
   phone=request.data['phone']
   last_name=request.data['last_name']
   image=request.data['image']
   role=request.data['role']
   id=request.data['department']
   dep=Department.objects.get(id=id)
   if email:
        if CustomUser.objects.filter(email=email).exists():
            response_data = {
                "status": 400,
                "message": "Email already exists"
            }
            return Response(response_data)

        password = str(random.randint(100000, 999999))
        subject = 'Your password'
        message = f"Your password is {password}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

        user = CustomUser.objects.create_user(
            email=email, phone=phone, password=password, image=image, 
            last_name=last_name, username=username, role=role,dep=dep
        )
        user.save()
        response_data = {
            "status": 200,
            "message": "Success"
        }
   else:
        response_data = {
            "status": 400,
            "message": "Email field is required"
        }

   return Response(response_data)



@api_view(['POST'])
@permission_classes([AllowAny])
def SignupPh(request):
   email=request.data['email']
   username=request.data['username']
   phone=request.data['phone']
   last_name=request.data['last_name']
   image=request.data['image']
   role=request.data['role']
   if email:
        if CustomUser.objects.filter(email=email).exists():
            response_data = {
                "status": 400,
                "message": "Email already exists"
            }
            return Response(response_data)

        password = str(random.randint(100000, 999999))
        subject = 'Your password'
        message = f"Your password is {password}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

        user = CustomUser.objects.create_user(
            email=email, phone=phone, password=password, image=image, 
            last_name=last_name, username=username, role=role
        )
        user.save()
        response_data = {
            "status": 200,
            "message": "Success"
        }
   else:
        response_data = {
            "status": 400,
            "message": "Email field is required"
        }

   return Response(response_data)



@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
     username=request.data['email']
     password=request.data['password']

     user=authenticate(username=username,password=password)

     if user is not None:
          token,created=Token.objects.get_or_create(user=user)
          response_data={
               'status':200,
               'token':token.key,
               'is_admin':user.is_staff,
               'role':user.role
          }
     else:
          response_data={
               'status':201,
               'message':"username and Password  doesn't Match"
          }
     return Response(response_data)






@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Active(request,id):
     user=CustomUser.objects.get(id=id)
     if user:
          user.is_active= not user.is_active
          user.save()
          response_data={
               'status':200,
               'message':'success'
          }
     else: 
          response_data={
               'status':201,
               'message':'user is inactive'
          }
     return Response(response_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Changepass(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({
            'status': 400,
            'message': 'Both old and new passwords are required.'
        }, status=400)

    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response({
            'status': 200,
            'message': 'Password changed successfully.'
        })
    else:
        return Response({
            'status': 401,
            'message': 'Old password is not correct.'
        }, status=401)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ChangepassP(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({
            'status': 400,
            'message': 'Both old and new passwords are required.'
        }, status=400)

    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response({
            'status': 200,
            'message': 'Password changed successfully.'
        })
    else:
        return Response({
            'status': 401,
            'message': 'Old password is not correct.'
        }, status=401)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ChangepassA(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({
            'status': 400,
            'message': 'Both old and new passwords are required.'
        }, status=400)

    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response({
            'status': 200,
            'message': 'Password changed successfully.'
        })
    else:
        return Response({
            'status': 401,
            'message': 'Old password is not correct.'
        }, status=401)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AllUser(request):
    # Get the authenticated user
    user = request.user
    user_image = CustomUser.objects.get(id=user.id)
    user_serializer = userSerializer(user_image)  # Serialize single user data

    # Get all users and serialize them
    users = CustomUser.objects.all()
    all_users_serializer = userSerializer(users, many=True)  # Serialize list of users

    response_data = {
        "Status": 200,
        "data": all_users_serializer.data,  # Serialized list of all users
        "user": user_serializer.data        # Serialized single authenticated user
    }

    return Response(response_data)




from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UpdateUser(request, id):
    instance = get_object_or_404(CustomUser, id=id)
    data = request.data.copy()
    
    # Retain the existing image if none is provided
    if not data.get('image'):
        data['image'] = instance.image

    # Update fields without validation
    instance.username = data.get('username', instance.username)
    instance.email = data.get('email', instance.email)
    instance.phone = data.get('phone', instance.phone)
    instance.image = data.get('image', instance.image)
    instance.save()
    
    response_data = {
        "status": status.HTTP_200_OK,
        "message": "User updated successfully",
        "data": {
            "username": instance.username,
            "email": instance.email,
            "phone": instance.phone,
            "image": str(instance.image.url) if instance.image else None
        }
    }
    
    return Response(response_data, status=status.HTTP_200_OK)