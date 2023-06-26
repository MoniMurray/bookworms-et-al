from django.shortcuts import render
from .models import Signup
from .forms import SignupForm

from django.contrib import messages


# Create your views here.
def signup(request):
    """
    A view to create a user signup
    """
    
    subscriber = []
    template = 'newsletter/signup.html'
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have been added to VIP Club')
        else: 
            messages.error(request, 'Please ensure the form is completed')

    context = {
        'form': form,
    }

    # if request.method == 'POST':
    #     email = request.POST.get('email', None)
    #     name = request.POST.get('name', None)

    #     if not email:
    #         messages.error(request, 'Please enter a valid email address') 
    #         return render('Signup/')

    #     subscriber.save()
    #     messages.success(request, 'You are successfully subscribed')

    return render(request, template, context)
    