from django.shortcuts import render


def login_view(request):
    """ login view """
    return render(request, 'account/login.html', {})


def register_view(request):
    """ register view """
    return render(request, 'account/register.html', {})
