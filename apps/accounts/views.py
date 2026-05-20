from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlsafe_base64_decode

from .forms import AddressForm, ProfileForm, RegistrationForm, UserForm
from .models import Address


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Account created. Email verification is ready for SMTP configuration.')
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, uidb64, token):
    user = get_object_or_404(User, pk=urlsafe_base64_decode(uidb64).decode())
    if default_token_generator.check_token(user, token):
        user.profile.email_verified = True
        user.profile.save()
        messages.success(request, 'Email verified.')
    return redirect('dashboard')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'orders': request.user.orders.all()[:5]})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def addresses(request):
    form = AddressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        messages.success(request, 'Address saved.')
        return redirect('addresses')
    return render(request, 'accounts/addresses.html', {'form': form, 'addresses': request.user.addresses.all()})


@login_required
def delete_address(request, pk):
    get_object_or_404(Address, pk=pk, user=request.user).delete()
    messages.info(request, 'Address deleted.')
    return redirect('addresses')

# Create your views here.
