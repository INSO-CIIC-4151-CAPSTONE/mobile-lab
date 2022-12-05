from django.contrib.auth import login, logout
from django.core.checks import messages
from django.core.exceptions import DisallowedRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import *

# Create your views here.
from app.models import User, Test, Request
from app.models import Message
from app.forms import RequestForm


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
                                                last_name=last_name, role='Patient')
                user.save()

                user = authenticate(request, username=email, password=password1)

                if user is not None:
                    login(request, user)
                    return redirect('profile')

            except IntegrityError:
                print("Integrity Error")

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.Info(request, 'Invalid Username or Password')
            return redirect("/")

    return render(request, 'login.html')


def home_view(request):
    return render(request, 'home.html')


def profile_view(request):
    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('/')

    name = request.user.first_name + ' ' + request.user.last_name
    context = {'name': name,
               'gender': request.user.gender,
               'address': request.user.address,
               'phone-number': request.user.phone_number,
               }
    return render(request, 'profile.html', context)


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message_str = request.POST['message']

        message_obj = Message.objects.create(name=name, email=email, message=message_str)

        message_obj.save()
        messages.Info(request, 'Message sent!')
        return redirect('/')

    return render(request, 'contact.html')


def test_view(request):
    tests = Test.objects.all()
    return render(request, 'catalog.html', {'tests': tests})


def createTestRequest(request):
    form = RequestForm()
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, "request_form.html", context)


def updateTestRequest(request, id):
    order = Request.objects.get(id=id)
    form = RequestForm(instance=order)

    if request.method == 'POST':
        form = RequestForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, "request_form.html", context)


def deleteTestRequest(request, id):
    order = Request.objects.get(id=id)
    context = {'item': order.lab_test.name}
    return render(request, 'delete_request.html', context)
