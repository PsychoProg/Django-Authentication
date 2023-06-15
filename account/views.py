from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm


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
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('account:login_url')
            else:
                form.add_error('phone', 'invalid phone number!!!')

        # else:
            # form.add_error('phone', 'invalid data!!!')
            # return redirect('account:login_url')

        return render(request, 'account/login.html', context)


