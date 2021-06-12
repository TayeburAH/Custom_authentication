from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Customer,Division, City, Zip

User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the custom User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email_phone', 'date_joined', 'get_full_name', 'last_joined', 'is_active', 'is_admin',
                    'is_customer',
                    'is_admin', 'is_seller',]
    list_filter = ['date_joined', 'email_phone']
    fieldsets = (
        (None, {'fields': ('email_phone', 'password')}),
        ('Personal info', {'fields': ('profile_image', 'first_name', 'last_name','otp')}),
        ('Permissions', {'fields': ('is_admin', 'is_customer', 'is_seller')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email_phone', 'password1', 'password2')}  # add required field
         ),
    )
    search_fields = ['email_phone']
    ordering = ['email_phone']
    readonly_fields = ('id', 'date_joined', 'last_joined','otp')  # to prevent from changing
    filter_horizontal = ()


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['__str__']


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Division)
admin.site.register(City)
admin.site.register(Zip)
