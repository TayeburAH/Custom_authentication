import shutil
import os

from django.db import transaction
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver
from allauth.account.admin import EmailAddress
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from .models import *

User = settings.AUTH_USER_MODEL

from allauth.account.signals import user_signed_up


# Usually pre_delete is used to clean up, the folder after delete() is clicked


@receiver(pre_delete, sender=User)  # post_delete : you have to delete twice
# as the instance still exist after the save()
def delete_folder(sender, instance, *args, **kwargs):
    try:  # instance.profile_image.delete()  will delete your default.png
        path = os.path.join(os.getcwd(), f'media\profile_images\{instance.pk}')
        shutil.rmtree(path)

    except OSError:
        pass


# pre_save.connect(delete_folder, sender=settings.AUTH_USER_MODEL)
# If you want to register the receiver function to several signals you may do it like this:
# @receiver([post_save, post_delete], sender=User)
# signal does not work when using it in a separate file

# When account is created via social, fire django-allauth signal to populate Django User record.
@receiver(user_signed_up)
@transaction.atomic
def populate_profile(request, sociallogin, user, **kwargs):
    """Signal, that gets extra data from sociallogin and put it to profile."""

    if sociallogin.account.provider == 'facebook':
        user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        email = user_data['email'].lower()
        first_name= user_data['first_name']
        last_name = user_data['last_name']

    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        email = user_data['email']

        first_name= " ".join(user_data['name'].split(' ')[0:-1])
        last_name = user_data['name'].split(' ')[-1]

    user.email_phone = user.email = email  # saves in both User, Social Account, User account
    user.is_customer = True
    user.save()

    # Email verification is auto with google but not for facebook
    # so we need to check our user is verifed or not
    if user.emailaddress_set.filter(verified=False).exists():
        account = EmailAddress.objects.get(email=user.email, verified=False)
        account.verified = True
        account.save()
    # now make a customer dor the corresponding user
    customer = Customer.objects.create(user=user)
    # student.attributes=self.cleaned_data.get(' attributes ')
    # Form must have this new attributes forms.charfield
    customer.first_name = first_name
    customer.last_name = last_name
    customer.save()
    return customer

    '''
    To access any instance data sociallogin
    sociallogin.account.extra_data['picture']
    sociallogin.account.uid
    sociallogin.account.provider
    sociallogin == socialacount table
    etc
    
    '''
