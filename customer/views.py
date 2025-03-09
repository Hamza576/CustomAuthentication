from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def customer_dashboad(request):
    return render(request, "customer/dashboard.html")

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password Changed Successfully. Login Again!")
            logout(request)
            return redirect('login')
    else: 
        form = PasswordChangeForm(user=request.user)

    return render(request, 'customer/passwordChange.html', {'form': form})