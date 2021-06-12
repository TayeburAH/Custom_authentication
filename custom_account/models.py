from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import pre_delete

from django.dispatch import receiver
from django.utils.safestring import mark_safe

from .custom_validators import *
import os
from PIL import Image
import shutil


# Create your models here.

# <------------------  Manager ------------------------->
class UserManager(BaseUserManager):
    def create_user(self, email_phone, password=None):
        """
        Creates and saves a User with the given email and password.
        You need to use validation
        """
        user = self.model(
            email_phone=email_phone,
        )

        user.set_password(password)  # or put it in   user = self.model( password = password)
        user.is_staff = False
        user.is_admin = False
        user.is_customer = False
        user.is_seller = False
        user.is_active = True
        # last save it
        user.save(using=self._db)
        return user

    def create_superuser(self, email_phone, password):
        """
        Creates and saves a superuser with the given email and password.
        No need to validate
        """

        user = self.create_user(
            email_phone=email_phone,
            password=password,

        )
        user.is_staff = True
        user.is_admin = True
        user.is_customer = True
        user.is_seller = True

        # last save it
        user.save(using=self._db)
        return user


# <------------------   User ------------------------->

# Saving profile image
def profile_image_file_path(self, filename):
    return f'profile_images/{self.pk}/{self.username}_{"profile_image.png"}'


# Default profile image
def default_image_file_path():
    return 'default_profile_image/default.png'


class User(AbstractBaseUser, PermissionsMixin):
    email_phone = models.CharField(
        verbose_name='Email or mobile number',  # to show its name in admin
        max_length=50,
        unique=True, validators=[validate_phone_number_or_email, ]  # list your own validator func here

    )
    email = models.CharField(verbose_name='Email',max_length=50,null=True,blank=True)
    phone = models.CharField(verbose_name='Phone', max_length=50,null=True,blank=True)

    date_joined = models.DateField(verbose_name='date joined',
                                   auto_now_add=True)  # when custom_account gets created the date gets set
    last_joined = models.DateField(verbose_name='last joined',
                                   auto_now=True)  # when custom_account gets created the date gets set

    # Extra fields goes under here
    # Extra fields to put in personal information
    # username = models.CharField(max_length=60, unique=True)
    otp = models.CharField(max_length=4, null=True,blank=True)

    profile_image = models.ImageField(upload_to=profile_image_file_path, default=default_image_file_path, null=True,
                                      blank=True)
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)

    # Must include
    is_active = models.BooleanField(default=True)  # only this true
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_admin = models.BooleanField(default=False)  # a superuser

    # add more multi_user
    is_customer = models.BooleanField(default=False)  # a customer
    is_seller = models.BooleanField(default=False)  # a seller

    # notice the absence of a "Password field", id, last_login that is built in.

    objects = UserManager()  # To link it with UserManager(BaseUserManager)

    USERNAME_FIELD = 'email_phone'
    # REQUIRED_FIELDS = ['username']  # Besides email what must be required

    def __str__(self):
        return self.email_phone  # Django uses this when it needs to convert the object into string

    def get_full_name(self):
        # The user is identified by their email address
        return f"{self.first_name} {self.last_name}"

    @property
    def profile_imgURL(self):  # you can also use {{ user.profile_image.url }}
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        try:  # initially it will have a default_profile_image/default.png, no profile_image.path
            img = Image.open(self.profile_image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)
        except ValueError:
            print('No folder')

    def image_tag(self):  # use image_tag in list_display
        if self.profile_image:
            return mark_safe('<img src="/media/%s" width="50" height="50" />' % self.profile_image)
        else:
            return mark_safe('<img src="/media/default.jpg" width="50" height="50" />')

    image_tag.short_description = 'Profile image'  # name of the column will be now Pictures

    # add more function here

    # Must be included
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # Works fine
    #  # deletes the old picture when updating it
    # def save(self, *args, **kwargs):
    #     try:
    #         this = User.objects.get(id=self.pk)  # getting the old picture
    #         if this.profile_image != self.profile_image:
    #             this.profile_image.delete()
    #     except:
    #         pass
    #     super(User, self).save(*args, **kwargs)  # carry on with normal save method

    # # Works fine
    # def delete(self, *args, **kwargs):
    #     try:  # Delete the data before
    #         self.profile_image.delete()  # django clan up isnit fast enough
    #         os.rmdir(os.path.join(os.getcwd(), f'media\profile_images\{self.pk}'))
    #     except FileNotFoundError:
    #         pass
    #     super(User, self).delete(*args, **kwargs)  # carry on with normal delete method


# @receiver(pre_delete, sender=User)  # post_delete : you have to delete twice
# # as the instance still exist after the save()
# def delete_folder(sender, instance, *args, **kwargs):
#     try:  # instance.profile_image.delete()  will delete your default.png
#         path = os.path.join(os.getcwd(), f'media\profile_images\{instance.pk}')
#         shutil.rmtree(path)
#
#     except OSError:
#         pass


# Customer information
class Division(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class City(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Zip(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)  # city_id
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'Zip Codes'

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name=' last login', auto_now=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    zip = models.ForeignKey(Zip, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.first_name


'''
AUTH_USER_MODEL = 'custom_account.User'    #<app_name>.custom_model_name
change from built-in user model to ours
'''

'''
'django_cleanup',
pip install django-cleanup

Instruction to delete files in Django
pip install django - cleanup
INSTALLED_APPS = (
    ...
    'django_cleanup',  # should go after your apps

'''

'''
Now you can't use  from django.contrib.auth.models import User
but you have to use 

from django.conf import settings
User = settings.AUTH_USER_MODEL
'''

'''
In other models, 
Example user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

So Copy this now
from django.conf import settings
User = settings.AUTH_USER_MODEL

or use

from django.contrib.auth import get_user_model
User = get_user_model()
'''

'''
to point it out to static directory, create it

settings.py
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # look for static directory
]
'''

'''
MEDIA_URL = '/media/'                       # to make a url
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
 This is where we are going to upload the pictures into the database, and stores it in media_cdn

 STATIC_ROOT is missing as its only needed when you upload in server
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, '')
 to upload the pictures into the database, but keep it 'static/images'

BASE_DIR = 'http://127.0.0.1:8000'

'''

'''
For media files
In root urls.py 

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    pip install Pillow

'''
