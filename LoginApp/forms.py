#from click import UsageError
from django import forms
from django.forms.fields import CharField
from django.forms.widgets import PasswordInput
from .models import UserModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class LoginForm(forms.Form):
    userid = forms.CharField(max_length=128, empty_value="Email or Mobile")
    password = forms.CharField(widget=PasswordInput())


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput(), max_length=128)
    confirm_password = forms.CharField(
        widget=PasswordInput(), label='confirm password', max_length=128)

    class Meta:
        model = UserModel
        fields = [
            'first_name', 'last_name',
            'email', 'mobile',
            'password', 'confirm_password'
        ]

    def clean(self, *args, **kwargs):
        cd = self.cleaned_data  # cleaned Data
        fields = [
            'first_name', 'last_name',
            'email', 'mobile',
        ]

        print("avdhut ", type(cd))

        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError("Password Mis-Match")
        if cd['email'] in UserModel.objects.filter(email=cd['email']):
            raise forms.ValidationError('username exist')
        if cd['mobile'] in UserModel.objects.filter(mobile=cd['mobile']):
            raise forms.ValidationError('username exist')

        return super(RegistrationForm, self).clean(*args, **kwargs)




class ForgetpasswordForm(forms.Form):
    email = forms.EmailField(max_length=50)


class PasswordCheckForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['password']

    def clean(self, *args, **kwargs):
        password = self.cleaned_data['password']
        user = kwargs["user"]
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect Password")


class ChangepasswordForm(forms.Form):
    new_password = forms.CharField(widget=PasswordInput(),max_length=30)
    confirm_password = CharField(widget=PasswordInput(),max_length=30)

    def clean(self, *args, **kwargs):
        cd = self.cleaned_data

        if cd['new_password'] != cd['confirm_password']:
            raise forms.ValidationError("Passowrd Didnt Match!!!!!!")

        return super(ChangepasswordForm, self).clean(*args, **kwargs)




class Profile(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'mobile']


#Roles = [('emp', 'emp'), ('admin', 'admin'), ('hr', 'hr')]
class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput(), max_length=128)
    confirm_password = forms.CharField(
        widget=PasswordInput(), label='confirm password', max_length=128)

    class Meta:
        model = UserModel
        fields = [
            'first_name', 'last_name',
            'email', 'mobile','role',
            'password', 'confirm_password'
        ]

    def clean(self, *args, **kwargs):
        cd = self.cleaned_data  # cleaned Data
        fields = [
            'first_name', 'last_name',
            'email', 'mobile',
        ]

        print("avdhut ", type(cd))

        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError("Password Mis-Match")
        
        if cd['email'] in UserModel.objects.filter(email=cd['email']):
            raise forms.ValidationError('username exist')
        if cd['mobile'] in UserModel.objects.filter(mobile=cd['mobile']):
            raise forms.ValidationError('username exist')

        return super(AddUserForm, self).clean(*args, **kwargs)


class UpdateForm(forms.ModelForm):
    class Meta:
        model= UserModel
        fields = [
            'first_name', 'last_name',
            'email', 'mobile','role'
        ]

class PasswordForm(forms.Form):
    password = forms.CharField(widget=PasswordInput(), max_length=128)
    confirm_password = forms.CharField(widget=PasswordInput(), max_length=128)

    def clean(self, *args, **kwargs):
        cd = self.cleaned_data

        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError("Passowrd Didnt Match!!!!!!")

        return super(PasswordForm, self).clean(*args, **kwargs)