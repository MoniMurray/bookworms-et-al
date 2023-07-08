from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Signup
from .forms import SignupForm


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
            messages.success(
                request, 'You have been added to VIP Club')
        else:
            messages.error(
                request, 'Please ensure the form is completed')
        return redirect(reverse('home'))

    context = {
        'form': form,
    }

    return render(request, template, context)
