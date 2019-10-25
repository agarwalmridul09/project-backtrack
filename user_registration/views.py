from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from user_registration.forms import LoginForm, SignUpForm
from user_registration.models import User


def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect("/productBacklog")
            else:
                return render(request, 'login.html',
                              {'form': form, 'error_message': "Please enter valid email-id and password"})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def view_404(request, exception):
    return redirect('/login')


def sign_up_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(email=form.cleaned_data['email'],
                                         password=form.cleaned_data['password'],
                                         first_name=form.cleaned_data['first_name'],
                                         last_name=form.cleaned_data['last_name'],
                                         role=form.cleaned_data['role'],
                                         )
                return redirect('/login/')
            except Exception as e:
                return render(request, 'sign_up.html',
                              {'form': form, 'error_message': e})
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
