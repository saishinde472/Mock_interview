from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserUpdateForm
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

def user_management(request):
    users = User.objects.all()
    return render(request, 'admin_panel/user_management.html', {'users': users})

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')  # Redirect to user management page after update
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'admin_panel/update_user.html', {'form': form})