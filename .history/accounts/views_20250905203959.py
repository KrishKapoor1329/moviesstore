from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your views here.

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home.index')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})
