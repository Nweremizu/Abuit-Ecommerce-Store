from django.shortcuts import render, redirect
from abuit_user.forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User


# Create your views here.
def redirect_entry(request):
    return redirect('core:main')

def register(request):
    if request.user.is_authenticated:
        return redirect("core:main")
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"New Account Created: {username}")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect("abuit_user:login")
        return render(request, "auth/register.html", {"form": form, })
    else:
        form = UserRegisterForm()
    context = {
        "form": form
    }
    return render(request, "auth/register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:main")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if remember_me:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                login(request, user)
                messages.success(request, "You're Logged In.")
                return redirect('core:main')
            else:
                messages.warning(request, "Wrong username or password")
                return redirect('abuit_user:login')
        except:
            messages.warning(request, f"User with {email} doesn't exist.")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You're Logged In.")
            return redirect('core:main')
        else:
            messages.warning(request, "Wrong username or password")
            return redirect('abuit_user:login')

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You Logged Out")
    return redirect('abuit_user:login')
