from django.contrib.auth import login, logout
from django.core.checks import messages
from django.core.exceptions import DisallowedRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.db import *
from app.models import User, Test, Request
from app.models import Message

''' © 2022 Mobile-Lab, All Rights Reserved. '''


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


def login_page(request):
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


def home_page(request):
    return render(request, 'home.html')


def profile_page(request):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('/')

    name = request.user.first_name + ' ' + request.user.last_name
    context = {'name': name,
               'gender': request.user.gender,
               'address': request.user.address,
               'phonenumber': request.user.phone_number,
               }
    return render(request, 'profile.html', context)


def about_page(request):
    return render(request, 'about.html')


def contact_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message_str = request.POST['message']

        message_obj = Message.objects.create(name=name, email=email, message=message_str)

        message_obj.save()
        messages.Info(request, 'Message sent!')
        return redirect('/')

    return render(request, 'contact.html')


def user_contact_page(request):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('/')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message_str = request.POST['message']

        message_obj = Message.objects.create(name=name, email=email, message=message_str)

        message_obj.save()
        messages.Info(request, 'Message sent!')

    return render(request, 'usercontact.html')


def labTests(request):
    tests = Test.objects.all()
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('/')
    return render(request, 'catalog.html', {'tests': tests})


def testList_page(request):
    tests = Test.objects.all()
    return render(request, 'testsList.html', {'tests': tests})


def createTestRequest(request, id):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    name = Test.objects.filter(id=id).get().name
    current_user = User.objects.filter(role='Patient').get(id=request.user.id)

    if request.method == 'POST':
        lab_test = Test.objects.get(id=id)
        modality = request.POST['modality']
        date = request.POST['date']
        hour = request.POST['hour']

        request_obj = Request.objects.create(lab_test=lab_test, modality=modality, date=date, hour=hour,
                                             patient=current_user)

        request_obj.save()

        messages.Info(request, 'Test requested!')
        return redirect('profile')

    return render(request, 'request_form.html', {'name': name})


'''def updateTestRequest(request, id):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    order = Request.objects.get(id=id)
    form = RequestForm(instance=order)

    if request.method == 'POST':
        form = RequestForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, "request_form.html", context)


def deleteTestRequest(request, id):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    order = Request.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('profile')
    context = {'item': order.lab_test.name}
    return render(request, 'delete_request.html', context)'''
