from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    
    fieldsets = (
        (None, {'fields': ('email', 'password','mobile')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name' , 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name', 'mobile','password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name','mobile','role', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name','mobile')
    ordering = ('email',)


admin.site.register(get_user_model(), CustomUserAdmin)

# Register your models here.
"""
site_title = _('My site admin')
    site_header = _('Administration')
    index_title = _('CustomLogin')
    #registering Custom login form for the Login interface
    #this login form uses CustomBackend
    login_form = CustomLoginForm
class CustomUserAdmin(UserAdmin):
    model = UserModel
    add_form = RegistrationForm
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(UserModel, CustomUserAdmin)
"""
#admin.site.register(UserModel)