from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('meteorite:homepage')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('meteorite:homepage')  # Jump to login after successful registration
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('meteorite:homepage')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('meteorite:homepage')  # Jump to homepage after successful login
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('meteorite:homepage')  # Jump to homepage after logging out

@login_required
def profile(request):
    return render(request, 'user/profile.html')