"""
Authentication views: Login, Register, Home
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User
from .forms import LoginForm, RegisterForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator



def home(request):
    """Home/Landing page"""
    return render(request, 'accounts/home.html')


@require_http_methods(["GET", "POST"])
def user_login(request):
    """Login view with role selection (USERNAME based)"""

    if request.user.is_authenticated:
        return redirect('accounts:login_redirect')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                if user.role != role:
                    messages.error(request, 'Selected role does not match this user.')
                else:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('accounts:login_redirect')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# @require_http_methods(["GET", "POST"])
# def user_register(request):
#     """Registration view with role selection and location capture"""

#     if request.user.is_authenticated:
#         return redirect('accounts:login_redirect')

#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             latitude = request.POST.get('latitude')
#             longitude = request.POST.get('longitude')
#             location_name = request.POST.get('location_name', '')

#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])

#             if latitude and longitude:
#                 user.latitude = latitude
#                 user.longitude = longitude
#                 user.location_name = location_name

#             user.save()

#             login(request, user)
#             messages.success(
#                 request,
#                 f'Registration successful! Welcome to LifeLink, {user.username}!'
#             )
#             return redirect('accounts:login_redirect')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = RegisterForm()

#     return render(request, 'accounts/register.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm
from .models import EmailOTP


@require_http_methods(["GET", "POST"])
def user_register(request):
    """Registration view with role selection, location capture, and OTP verification"""

    if request.user.is_authenticated:
        return redirect('accounts:login_redirect')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']

            # 🔐 OTP VERIFICATION CHECK (NEW)
            otp_obj = EmailOTP.objects.filter(
                email=email,
                is_verified=True
            ).first()

            if not otp_obj:
                messages.error(request, "Please verify your email using OTP before registering.")
                return redirect('accounts:register')

            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            location_name = request.POST.get('location_name', '')

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])

            if latitude and longitude:
                user.latitude = latitude
                user.longitude = longitude
                user.location_name = location_name

            user.save()

            # OPTIONAL: clean OTP after successful registration
            otp_obj.delete()

            login(request, user)

            messages.success(
                request,
                f'Registration successful! Welcome to LifeLink, {user.username}!'
            )
            return redirect('accounts:login_redirect')

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})





















def login_redirect(request):
    """Redirect user to their role-specific dashboard"""

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.role == 'donor':
        return redirect('donors:dashboard')
    elif request.user.role == 'bloodbank':
        return redirect('bloodbanks:dashboard')
    elif request.user.role == 'patient':
        return redirect('patients:dashboard')

    return redirect('accounts:home')


def user_logout(request):
    """Logout view"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:home')

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from accounts.models import EmailOTP


from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP


@require_POST
def send_otp(request):
    email = request.POST.get('email')

    if not email:
        return JsonResponse({
            'success': False,
            'message': 'Email is required'
        })

    otp_obj, created = EmailOTP.objects.get_or_create(email=email)
    otp_obj.is_verified = False   # reset if resend
    otp_obj.generate_otp()
    otp_obj.save()

    try:
        send_mail(
            subject='LifeLink OTP Verification',
            message=f'Your OTP for LifeLink registration is: {otp_obj.otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,  # 🔥 FIXED
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        print("OTP EMAIL ERROR:", e)
        return JsonResponse({
            'success': False,
            'message': 'Failed to send OTP. Try again.'
        })

    return JsonResponse({
        'success': True,
        'message': 'OTP sent successfully'
    })


@require_POST
def verify_otp(request):
    email = request.POST.get('email')
    otp = request.POST.get('otp')

    if not email or not otp:
        return JsonResponse({
            'success': False,
            'message': 'Email and OTP required'
        })

    try:
        otp_obj = EmailOTP.objects.get(email=email)

        if otp_obj.otp == otp:
            otp_obj.is_verified = True
            otp_obj.save()

            return JsonResponse({
                'success': True,
                'message': 'OTP verified successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid OTP'
            })

    except EmailOTP.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'OTP not found'
        })
