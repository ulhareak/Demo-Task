from logging import raiseExceptions
from django.shortcuts import render, redirect, render_to_response
#from pyrsistent import T
from . import forms
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserModel as User
import uuid
from django.contrib import messages
from . import helperfunctions
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from .backends import CustomBackend
from django.views.decorators.csrf import csrf_exempt
#from .forms import AddUser as UpdateForm


uuid_token = ""
user_object = ""
backend = CustomBackend()
c_token = ''


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
                print("in login , ", user, password)
                user = authenticate(request, email=userid, password=password)
                print("login try ", user.id, user.email)
            except:
                print("Login Exception ")
                return redirect("LoginApp:login")

            if user is not None:
                login(request, user)
                Users = User.objects.all()
                context = {'Users': Users, 'User': user}
                print("Role", user.role, user.first_name)
                role = ['admin', 'hr']
                if user.role in role:
                    return render(request, 'LoginApp/adminsite.html', context)
                else:
                    return render(request, 'LoginApp/user_details.html', context)

    return render(request, 'LoginApp/login.html', {'form': forms.LoginForm()})


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
        new_user = authenticate(email=user.email, password=password)
        login(request, new_user)

        if next:
            return redirect(next)
        return redirect('/')

    return render(request, 'LoginApp/signup.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('/')


def admin_logout(request):
    logout(request)
    return redirect("/")


def forgetpassword_view(request):

    if request.method == 'POST':
        form = forms.ForgetpasswordForm(request.POST or None)
        if form.is_valid():
            entered_email = form.cleaned_data.get('email')
            user = ""
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
            # print(username)
            if user is None or uuid_token != token:
                messages.success(request, " User Not found ")
                return redirect(f'changepassword/{token}/')

            user.set_password(new_password)
            user.save()
            return redirect('/login/')

    return render(request, 'LoginApp/change_password.html', {'form': forms.ChangepasswordForm()})

#update logged in user profile 
def userProfile(request, id):
    try:
        user = User.objects.get(Q(id=id))
    except:
        pass
    print("userProfile View ", user.first_name)
    print(request)
    if request.method == 'POST':
        form = forms.Profile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.save()
            Users = User.objects.all()
            template_name = ''
            if user.role in ["admin", 'hr']:
                template_name = 'adminsite.html'
            else:
                template_name = 'user_details.html'
            return render(request, 'LoginApp/'+template_name, {'Users': Users, 'current_user': user})
    else:
        pre_data = {'first_name': user.first_name, "last_name": user.last_name,
                    "email": user.email, "mobile": user.mobile}
        form = forms.Profile(initial=pre_data)

    return render(request, "LoginApp/profile.html", {'form': form, "current_user": user , 'request_user':user})


def delete(request, id):
    try:
        user = User.objects.get(Q(id=id))
    except:
        pass
    user.delete()
    Users = User.objects.all()
    print("Current user :", request.user.id)
    user = request.user
    context = {'Users': Users, 'User': user}
    return render(request, 'LoginApp/adminsite.html', context)


def update(request, id):
    from .forms import UpdateForm
    try:
        user = User.objects.get(Q(id=id))
        request_user = User.objects.get(id=request.user.id)
    except:
        pass
    print("Update View ", user.first_name)
    print(request)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if form.cleaned_data['role'] == 'admin':
                user.is_superuser = user.is_staff = True
            else :
                user.is_superuser = user.is_staff = False
            user.role = form.cleaned_data['role']
            # user.set_password(form.cleaned_data['password'])
            user.save()
            Users = User.objects.all()
            return render(request, 'LoginApp/adminsite.html', {'Users': Users, 'User': request_user})
    else:
        pre_data = {'first_name': user.first_name, "last_name": user.last_name,
                    "email": user.email, "mobile": user.mobile,  'role': user.role}
        form = UpdateForm(initial=pre_data)

    return render(request, "LoginApp/profile.html", {'form': form, "request_user": request_user , 'current_user':user })#,'':user })


def add(request, id):
    request_user = ''
    try:
        request_user = User.objects.get(Q(id=id))
    except:
        pass
    if request.method == "POST":
        form = forms.AddUserForm(request.POST or None)
        
        if form.is_valid() :
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm password')
            mobile = form.cleaned_data.get('mobile')
            user.role = form.cleaned_data['role']
            if form.cleaned_data['role'] == 'admin':
                user.is_superuser = True
            user.set_password(password)
            user.save()
            

            Users = User.objects.all()
            return render(request, 'LoginApp/adminsite.html', {'Users': Users, 'User': request_user})

    return render(request, 'LoginApp/adduser.html', {'user_form': forms.AddUserForm(), 'User':request_user})#, 'password_form': forms.PasswordForm(), 'User': request_user})


def change_password(request, id):
    try:
        user = User.objects.get(Q(id=id))
    except:
        pass

    if request.method == "POST":
        check_form = forms.PasswordCheckForm(request.POST or None)
        update_form = forms.ChangepasswordForm(request.POST or None)
        check_form.save(user=user)
        if user.check_password(check_form.cleaned_data['passowrd']):
            pass

    else:
        return render(request, 'LoginApp/change_password.html', {'check_form': forms.PasswordCheckForm(),
                                                                 'upadte_form': forms.ChangepasswordForm()})


def site(request, id):
    try:
        request_user = User.objects.get(Q(id=id))
        Users = User.objects.all()
    except:
        pass

    if (request_user.role in ['admin', 'hr']):
        return render(request, 'LoginApp/adminsite.html',  {'Users': Users, 'User': request_user})
    else:
        return render(request, 'LoginApp/user_details.html', {'Users': Users, 'User': request_user})
