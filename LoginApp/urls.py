from . import views
from django.urls import path

app_name = 'LoginApp'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('page/' , views.page , name='page'),
    path('signup/', views.signup_view, name='signup'),
    path('forgetpassword/', views.forgetpassword_view, name='forgetpassword'),
    path('changepassword/<token>/',
         views.change_password_view, name='changepassword'),
    path('logout/', views.logout_view, name='logout-user'),
    path('profile/' , views.userProfile ),
    path('delete/<int:id>/', views.delete),
    path('update/<int:id>/', views.update),
    path('add/' , views.add , name="add"),
]
