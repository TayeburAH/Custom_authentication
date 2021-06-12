from django.contrib.auth.views import PasswordContextMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail, BadHeaderError
from twilio.rest import Client
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.

def main(request):
    context = {}
    return render(request, 'main.html', context)


def send_otp(request):
    # OTP Code generate
    otp = str(random.randint(8000, 9000))
    # save otp in User model
    request.user.otp = otp
    request.user.save()
    print(otp)
    if request.user.email_phone.isnumeric():
        pass
        # #Twilio code
        # # Find your Account SID and Auth Token at twilio.com/console
        # # and set the environment variables. See http://twil.io/secure
        # account_sid = os.environ['TWILIO_ACCOUNT_SID']
        # auth_token = os.environ['TWILIO_AUTH_TOKEN']
        # client = Client(account_sid, auth_token)
        #
        # message = client.messages.create(
        #     body=f'Hi there! Your OTP number is {otp}',
        #     from_='+15017122661',
        #     to=f'{request.user.phone}'
        # )
        # print(message.sid)
    else:
        send_mail(
            # Subject
            'Helle from FoodMania',
            # Body
            f'Your OTP is {otp}. In order to activate your custom_account please type in the OTP',
            # From
            'tayebur@canadaeducationbd.com',
            # to
            ['takib687@gmail.com', request.user.email_phone, ],
            # What happens if it fails?
            fail_silently=True,

        )

    return redirect('otp_checker')


def otp_checker(request):
    if request.method == 'POST':
        if request.user.otp == request.POST.get('otp'):
            request.user.is_active = True
            request.user.save()
            messages.success(request, 'Account activated')
            logout(request)
            return redirect('login_process')
        else:
            messages.success(request, 'Wrong OTP')

    context = {
        'email_phone': request.user.email_phone,
    }
    return render(request, 'custom_account/otp.html', context)


def signup(request):
    if request.user.is_authenticated:  # always check whether logged in or not
        return redirect('home')
    else:
        form = CustomerForm()
        if request.method == 'POST':
            form = CustomerForm(request.POST or None)  # Pass in the data for validation
            if form.is_valid():  # to check and show form.errors in templates
                form.save()
                messages.success(request,
                                 'Account created')  # we dont have to pass it in, message is sent to all templates
                user = authenticate(request, email_phone=request.POST.get('email_phone'),
                                    password=request.POST.get('password2'))
                login(request, user)
                return redirect('send_otp')

        context = {'form': form}
        return render(request, 'custom_account/signup.html', context)


# make a login form, pass messages
# Name the input name = "email", name = "password"
def login_process(request):
    # Used HTML Raw Form
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            user = authenticate(request, email_phone=request.POST.get('email_phone'),
                                password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                if user.is_active:
                    return redirect('main')
                else:
                    return redirect('send_otp')
            else:
                messages.error(request, 'User or password incorrect.')

    context = {}  # no need to pass any form
    return render(request, 'custom_account/login.html', context)


def logout_process(request):
    logout(request)
    context = {}
    return redirect('login_process')


def edit_profile(request):
    customer = get_object_or_404(Customer, user=request.user)
    form = CustomerUpdateForm(instance=customer or None)
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST or None, instance=customer or None)
        if form.is_valid():  # to check and show form.errors in templates
            customer = form.save(commit=False)
            customer.user = request.user  # this is missing from form, so i have to save it
            # here as i need request.user which i cant get in super(Customer,self).save(commit=False)

            customer.address = form.cleaned_data.get('address')
            # since I redesigned the address field, I need to personally
            # save it
            customer.save()
            messages.success(request,
                             'Account Updated.')  # we don't have to pass it in, message is sent to all templates
            return redirect('edit_profile')

    context = {'form': form}
    return render(request, 'custom_account/edit_profile.html', context)


def delete_process(request):
    if request.method == 'POST':
        user = authenticate(request, email_phone=request.user.email_phone, password=request.POST.get('password'))
        if user is not None:
            user.delete()
            return redirect('main')
        else:
            messages.error(request, 'password incorrect')

    context = {}  # no need to pass any form
    return render(request, 'custom_account/delete_process.html', context)


# AJAX CITIES
def load_cities(request):
    division_id = request.GET.get('division_id')

    cities = City.objects.filter(division_id=division_id)
    # return render(request, 'persons/city_dropdown_list_options.html', {'cities': cities})
    return JsonResponse(list(cities.values('id', 'name')), safe=False)


# AJAX ZIPS
def load_zips(request):
    city_id = request.GET.get('city_id')
    zips = Zip.objects.filter(city_id=city_id)
    # return render(request, 'persons/city_dropdown_list_options.html', {'zips': zips})

    return JsonResponse(list(zips.values('id', 'name')), safe=False)


def password_reset_request(request):
    password_reset_form = PasswordResetForm()
    if request.method == "POST":
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email_phone']
            print(data)
            if '@' in data:
                user = User.objects.get(email=data.lower())

                # You can use more than one way like this for resetting the password.
                # ...filter(Q(email=data) | Q(username=data))
                # but with this you may need to change the password_reset form as well.

                # subject = "registration/password_reset_subject.txt" Does not seem to work
                subject = 'Request for password change'
                password_reset_email = "registration/password_reset_email.html"
                context = {
                    "email": user.email,
                    'domain': domain,
                    # 'site_name': site_name,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https',
                }

                email = render_to_string(password_reset_email, context)
                try:
                    send_mail(subject, email, 'tayebur@canadaeducationbd.com', [data], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect("password_reset_done")
            else:
                request.session['phone_number'] = data
                return redirect('forgot_password_otp_maker_checker')  # this is the link to set-password
                # forgot_password_otp_checker(otp,data)

    context = {"form": password_reset_form}
    return render(request, "registration/password_reset.html", context)


def forgot_password_otp_maker_checker(request):
    if request.method == 'GET':
        otp = str(random.randint(2000, 9000))
        request.session['otp'] = otp
        # If you want to use a variable, only use request.session
        # If you are ASSIGNING any variable, the variable will get
        # newly assigned everytime POST is submitted.

    if request.method == 'POST':
        print('hi', request.POST.get('otp'))
        if request.session['otp'] == str(request.POST.get('otp')):
            return redirect('forgot_password_otp_checker')
        else:
            messages.success(request, 'Wrong OTP')

    context = {
        'email_phone': request.session.get('phone_number'),
    }
    return render(request, 'custom_account/otp.html', context)


def forgot_password_reset(request):
    form = PasswordChange()
    if request.method == 'POST':
        form = PasswordChange(request.POST or None)
        if form.is_valid():
            phone = request.session.get('phone_number')
            user = User.objects.get(phone=phone)
            password = form.cleaned_data['new_password2']
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Updated.')
            return redirect('login_process')
    context = {"form": form}
    return render(request, "registration/password_reset_form.html", context)
