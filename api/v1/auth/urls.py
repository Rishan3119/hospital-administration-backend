from django.urls import path

from api.v1.auth import views

urlpatterns = [
   path('signup',views.Signup),
   path('signupP',views.SignupPh),
  path('login',views.Login),
  path('changePass',views.Changepass),
  path('changePassP',views.ChangepassP),
  path('changePassA',views.ChangepassA),
  path('alluser',views.AllUser),
  path('updateuser/<int:id>',views.UpdateUser)
]