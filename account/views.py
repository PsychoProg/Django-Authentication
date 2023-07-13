from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import LoginForm, RegisterForm, CheckOtpForm
from Authentication import settings
from random import randint
from .models import Otp, CustomUser
from django.utils.crypto import get_random_string


class UserLogin(View):
    def get(self, request):
        """ get method requests """
        form = LoginForm()
        context = {'form': form}
        return render(request, 'account/login.html', context)

    def post(self, request):

        form = LoginForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            # cleaned data = cd
            cd = form.cleaned_data
            # note: use username for authentication field
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('account:login_url')
            else:
                form.add_error('email', 'invalid email address!!!')

        # else:
            # form.add_error('phone', 'invalid data!!!')
            # return redirect('account:login_url')

        return render(request, 'account/login.html', context)


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'account/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            # email = form.cleaned_data.get('email')
            cd = form.cleaned_data
            email = cd["email"]
            rand_code = randint(10000, 99999)
            send_mail(
                'Verification code',
                f'code: {rand_code}',
                settings.EMAIL_HOST_USER,
                # reception
                [email],
                fail_silently=False,
            )
            print(rand_code)
            token = get_random_string(length=50)
            Otp.objects.create(token=token, email=email, pass_code=rand_code)
            # send email address via URL to check in in CheckOtpView(0
            # return redirect(reverse('account:check_otp_url') + f'?email={email}')     # use token instead of email
            return redirect(reverse('account:check_otp_url') + f'?token={token}')

        else:
            form.add_error('email', 'invalid email!!!')

        return render(request, 'account/register.html', context)


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        context = {'form': form}
        return render(request, 'account/check_otp.html', context)

    def post(self, request):
        # email = request.GET.get("email")
        token = request.GET.get("token")
        form = CheckOtpForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(token=token, pass_code=cd["code"]).exists():
                otp = Otp.objects.get(token=token)
                user = CustomUser.objects.create(email=otp.email)
                login(request, user)
                return redirect('/')
        else:
            form.add_error('email', 'invalid email!!!')

        return render(request, 'account/check_otp.html', context)
