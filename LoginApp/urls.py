from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

app_name = 'LoginApp'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('forgetpassword/', views.forgetpassword_view, name='forgetpassword'),
    path('changepassword/<token>/',
         views.change_password_view, name='changepassword'),
    path('logout/', views.logout_view, name='logout-user'),
    path('profile/<int:id>/' , views.userProfile ),
    path('delete/<int:id>/', views.delete),
    path('update/<int:id>/', views.update),
    path('add-user/<int:id>/' , views.add),
    path('site/<int:id>/', views.site),
    #path('admin/login/' ,views.login_view , name = 'admin'),
    path('admin/', admin.site.urls, name='admin'),
]
