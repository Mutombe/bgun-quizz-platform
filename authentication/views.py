from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from quizz.models import QuizProgress

def register(request):
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
    logout(request)
    return redirect('login')

def profile(request):
    progress = QuizProgress.objects.filter(user=request.user).order_by('-end_time')
    return render(request, 'profile/profile.html', {'progress': progress})
    
