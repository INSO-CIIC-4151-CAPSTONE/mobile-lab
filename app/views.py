from django.contrib.auth import login, logout
from django.core.exceptions import DisallowedRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.db import *

from app.forms import PatientForm, AddressForm, HealthForm
from app.models import User, Test, Request, Message
from django.contrib import messages

'''-----------------------------------© 2022 Mobile-Lab, All Rights Reserved.---------------------------------------'''

"""A view that displays the register page"""


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


"""A view that displays the login page"""


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.warning(request, 'Invalid Username or Password')
            return redirect("login")

    return render(request, 'login.html')


"""A view that displays the home page"""


def home_page(request):
    return render(request, 'home.html')


"""A view that displays the user profile page also, user can see request made"""


def profile_page(request):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('/')
    try:
        ppic = User.objects.filter(role='Patient').get(id=request.user.id).profile_picture.url
    except ValueError:
        ppic = "/static/images/user.png"

    current_patient = User.objects.filter(role='Patient').get(id=request.user.id)
    patient_request = Request.objects.filter(patient=current_patient).all()
    patient_full_name = request.user.first_name + ' ' + request.user.last_name

    context = {'user': current_patient, 'requests': patient_request,
               'name': patient_full_name, 'ppic': ppic}

    return render(request, 'profile.html', context)


"""A view that displays the about page, info of mobile lab and mission"""


def about_page(request):
    return render(request, 'about.html')


def settings_page(request):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('/')
    current_patient = User.objects.filter(role='Patient').get(id=request.user.id)
    try:
        ppic = current_patient.profile_picture.url
    except ValueError:
        ppic = "/static/images/user.png"

    form = PatientForm(instance=current_patient)
    form1 = AddressForm(instance=current_patient)
    form2 = HealthForm(instance=current_patient)

    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=current_patient)
        form1 = AddressForm(request.POST, instance=current_patient)
        form2 = HealthForm(request.POST, request.FILES, instance=current_patient)

        if form.is_valid() and form1.is_valid() and form2.is_valid():
            form.save()
            form1.save()
            form2.save()
            messages.success(request, 'Account settings updated!')
            return redirect('/profile')

    context = {'form': form, 'form1': form1, 'form2': form2, 'ppic': ppic}
    return render(request, 'user_settings.html', context)


"""A view that displays the contact page, this view is for not logged users. 
   Users can send messages to the company"""


def contact_page(request):
    e_pic = "/static/images/email.png"
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message_str = request.POST['message']
        subject = request.POST['subject']

        message_obj = Message.objects.create(name=name, email=email, message=message_str, subject=subject)

        message_obj.save()
        messages.success(request, 'Message sent!')
        return redirect('/contact')

    return render(request, 'contact.html', {'e_pic': e_pic})


"""A view that displays the contact page, this view is for logged users. 
   Users can send messages to the company"""


def user_contact_page(request):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    e_pic = "/static/images/email.png"
    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('/')
    user_email = request.user.email
    user_full_name = request.user.first_name + ' ' + request.user.last_name
    if request.method == 'POST':
        name = user_full_name
        email = user_email
        message_str = request.POST['message']
        subject = request.POST['subject']

        message_obj = Message.objects.create(name=name, email=email, message=message_str, subject=subject)

        message_obj.save()
        messages.success(request, 'Message sent!')

        return redirect('/usercontact')

    context = {'name': user_full_name, 'email': user_email,
               'e_pic': e_pic}

    return render(request, 'usercontact.html', context)


"""A view that displays the Test list page, this view is for not logged users. 
   Users can see a list with lab tests that the lab offers"""


def testList_page(request):
    tests = Test.objects.all()
    return render(request, 'testsList.html', {'tests': tests})


"""A view that displays the catalog page, this view is for logged users. 
   Users can select a lab test to request"""


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


"""A view that displays the a request test lab form page, this view is for logged users. 
   Users can select day,hour and modality of selected test"""


def createTestRequest(request, id):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('/')

    test = Test.objects.get(id=id)
    current_user = User.objects.filter(role='Patient').get(id=request.user.id)

    if Request.objects.filter(patient=current_user).exists() and Request.objects.filter(
            patient=current_user).get().lab_test == test:
        messages.info(request, "test already requested!")
        return redirect('profile')

    if request.method == 'POST':
        lab_test = test
        modality = request.POST['modality']
        date = request.POST['date']
        hour = request.POST['hour']

        request_obj = Request.objects.create(lab_test=lab_test, modality=modality, date=date, hour=hour,
                                             patient=current_user)

        request_obj.save()

        messages.success(request, 'Test requested!')
        return redirect('profile')

    return render(request, 'request_form.html', {'test': test})


"""A view that displays the a request test lab form page, this view is for logged users. 
   Users can update the selected day,hour and modality of selected test"""


def updateTestRequest(request, id):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('/')

    user_request = Request.objects.get(id=id)
    test = user_request.lab_test

    if request.method == 'POST':
        modality = request.POST['modality']
        date = request.POST['date']
        hour = request.POST['hour']

        user_request.lab_test = test
        user_request.requested_date = date
        user_request.hour = hour
        user_request.modality = modality

        user_request.save()
        messages.success(request, 'Test Updated!')
        return redirect('profile')

    return render(request, 'request_form.html', {'test': test})


"""A view that delete a selected requested lab test"""


def deleteTestRequest(request, id):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)
    request = Request.objects.get(id=id)
    request.delete()
    return redirect('profile')
