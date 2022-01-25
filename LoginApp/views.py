from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login, logout
from .models import UserModel as User
import uuid
from django.contrib import messages
from . import helperfunctions
from django.db.models import Q


uuid_token = ""
user_object = ""


def home_view(request):
    return render(request, 'LoginApp/home.html')


def login_view(request):
    form = forms.LoginForm(request.POST)
    user = None
    if request.method == "POST":
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']

            try:
                user = authenticate(request, email=userid, password=password)
            except:
                return redirect("LoginApp:login")

            if user is not None:
                login(request, user)
                print("Role", user.role, user.first_name)
                return redirect('/page/')

    return render(request, 'LoginApp/login.html', {'form': forms.LoginForm()})


def page(request):
    try:
        id = request.user.id
        request_user = User.objects.get(Q(id=id))
        Users = User.objects.all()
    except:
        pass
    context = {'Users': Users, 'User': request_user}
    if (request_user.role in ['admin', 'hr']):
        return render(request, 'LoginApp/adminsite.html', context)
    else:
        return render(request, 'LoginApp/user_details.html', context)


def signup_view(request):
    next = request.GET.get('next')

    form = forms.RegistrationForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        confirm_password = form.cleaned_data.get('confirm password')
        mobile = form.cleaned_data.get('mobile')
        user.role = 'emp'
        user.is_superuser = False
        user.set_password(password)
        user.save()
        return redirect('/login/')

    return render(request, 'LoginApp/signup.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('/')


def forgetpassword_view(request):

    if request.method == 'POST':
        form = forms.ForgetpasswordForm(request.POST or None)
        if form.is_valid():
            entered_email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=entered_email)
            except:
                user = None
            if not user:
                messages.success(request, 'User not  found with this email.')
                return redirect('/forgetpassword/')

            global uuid_token
            global user_object
            uuid_token = str(uuid.uuid4())
            user_object = user

            helperfunctions.send_forgertpassword_email(
                user_object.email, uuid_token)
            messages.success(request, 'An email is sent.')
            return redirect('/forgetpassword/')

    return render(request, 'LoginApp/forgetpassword.html', {'form': forms.ForgetpasswordForm()})


def change_password_view(request, token):
    if request.method == 'POST':
        form = forms.ChangepasswordForm(request.POST or None)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']

            try:
                user = User.objects.get(email=user_object.email)
            except:
                user = None
            if user is None or uuid_token != token:
                messages.success(request, " User Not found ")
                return redirect(f'changepassword/{token}/')

            user.set_password(new_password)
            user.save()
            return redirect('/login/')

    return render(request, 'LoginApp/change_password.html', {'form': forms.ChangepasswordForm()})

# update logged in user profile


def userProfile(request):
    try:
        user = User.objects.get(Q(id=request.user.id))
    except:
        pass
    print("userProfile View ", user.first_name)
    print(request)
    if request.method == 'POST':
        form = forms.Profile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.save()
            return redirect('/page/')
    else:
        pre_data = {'first_name': user.first_name, "last_name": user.last_name,
                    "email": user.email, "mobile": user.mobile}
        form = forms.Profile(initial=pre_data)

    return render(request, "LoginApp/profile.html", {'form': form, "current_user": user, 'request_user': user})


def delete(request, id):
    try:
        user = User.objects.get(Q(id=id))
    except:
        pass
    user.delete()
    return redirect('/page/')


def update(request, id):
    try:
        user = User.objects.get(Q(id=id))
    except:
        pass
    print("Update View ", user.first_name)
    print(request)
    if request.method == 'POST':
        form = forms.UpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if form.cleaned_data['role'] == 'admin':
                user.is_superuser = user.is_staff = True
            else:
                user.is_superuser = user.is_staff = False
            user.role = form.cleaned_data['role']
            user.save()
            return redirect('/page/')

    else:
        pre_data = {'first_name': user.first_name, "last_name": user.last_name,
                    "email": user.email, "mobile": user.mobile,  'role': user.role}
        form = forms.UpdateForm(initial=pre_data)

    return render(request, "LoginApp/profile.html", {'form': form, 'current_user': user})


def add(request):
    try:
        request_user = User.objects.get(Q(id=request.user.id))
    except:
        pass
    if request.method == "POST":
        form = forms.AddUserForm(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.mobile = form.cleaned_data.get('mobile')
            user.role = form.cleaned_data['role']
            if form.cleaned_data['role'] == 'admin':
                user.is_superuser = True
            user.set_password(password)
            user.save()
            return redirect('/page/')

    return render(request, 'LoginApp/adduser.html', {'user_form': forms.AddUserForm(), 'User': request_user})
