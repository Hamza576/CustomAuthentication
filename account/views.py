from django.shortcuts import render, redirect
from account.forms import RegistrationForm, LoginForm, PasswordResetForm
from django.contrib import messages
from django.conf import settings
from account.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm

# Sending email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_email, send_reset_password_email


# Create your views here.
def home(request):
    return render(request, "account/home.html")


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            # send email for account activation
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            # activation_link = f"{settings.SITE_DOMAIN}/activate/{uid}/token/"
            activation_link = reverse(
                "activate", kwargs={"uidb64": uidb64, "token": token}
            )
            activation_url = f"{settings.SITE_DOMAIN}{activation_link}"
            send_activation_email(user.email, activation_url)
            messages.success(request, "Account Created Successfully!")
            messages.success(
                request,
                "We have sent an email to your inbox. Please, Check email to activate your account.",
            )
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "account/register.html", {"form": form})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(pk=uid)

        if user.is_active:
            messages.warning(request, "Your account is already activated!")
            return redirect("login")

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                "Your account has been Successfully Activated! Now you can Login",
            )
            return redirect("login")
        else:
            messages.error(request, "The Activation Link is Invalid or has Expired.", extra_tags='danger')
            return redirect("login")

    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        messages.error(request, "Activation Link is Invalid!", extra_tags='danger')
        return redirect("login")

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect("seller_dashboard")
        elif request.user.is_customer:
            return redirect("customer_dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successfully!")
                if user.is_seller:
                    redirect("seller_dashboard")
                if user.is_customer:
                    return redirect("customer_dashboard")
            else:
                messages.error(request, "Not Logged In!", extra_tags='danger')
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                # send email for account activation
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = reverse(
                    "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
                )
                reset_url = f"{settings.SITE_DOMAIN}{reset_link}"
                send_reset_password_email(user.email, reset_url)
                messages.success(request, "We have sent an Password Reset link. Please check your Email Inbox!")
                return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, "account/password_reset.html", {'form': form})

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Your Password has been successfully Reset!")
                    return redirect('login')
            else:
                form = SetPasswordForm(user)

            return render(request, 'account/password_reset_confirm.html', {'form': form})
        else:
            messages.error(request, "The Password Reset Link is Invalid or has Expired.", extra_tags='danger')
            return redirect('password_reset')

    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        messages.error(request, "Link has Expired or is Invalid!", extra_tags='danger')
        return redirect("password_reset")