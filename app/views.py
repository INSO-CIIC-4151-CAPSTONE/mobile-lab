from django.contrib.auth import login
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import *


# Create your views here.
from app.models import Patient


def register_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username=email, email=email, password=password1, first_name=first_name,
                                                last_name=last_name)
                user.save()
                new_patient = Patient.objects.create(patient_user=user)
                new_patient.save()

                user = authenticate(request, username=email, password=password1)

                if user is not None:
                    login(request, user)
                    return redirect('profile.html')

            except IntegrityError:
                print("Integrity Error")

    return render(request, 'register.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/profile')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect("/")

    return render(request, 'login.html')


def home_page(request):
    return render(request, 'home.html')
