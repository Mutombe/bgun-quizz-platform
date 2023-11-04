from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from authentication.forms import UserProfileForm
from authentication.models import UserProfile
from quizz.models import QuizProgress
from django.contrib.auth.decorators import login_required

def register(request):
    """Register user account"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect('login')
            
    else:
        
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    """Login with user account"""
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def profile(request):
    """Render the profile for the user"""
    progress = QuizProgress.objects.filter(user=request.user).order_by('-end_time')
    return render(request, 'profile/profile.html', {'progress': progress})


@login_required
def edit_profile(request):
    """Edit the profile for the user"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile/edit_profile.html', {'form': form})
    
