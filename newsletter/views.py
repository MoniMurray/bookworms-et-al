from django.shortcuts import render
from .models import Signup

# Create your views here.
def signup(request):
    """
    A view to create a user signup
    """
    
    subscriber = []
    template = 'newsletter/signup.html'

    context = {}

    # if request.method == 'POST':
    #     email = request.POST.get('email', None)
    #     name = request.POST.get('name', None)

    #     if not email:
    #         messages.error(request, 'Please enter a valid email address') 
    #         return render('Signup/')

    #     subscriber.save()
    #     messages.success(request, 'You are successfully subscribed')

    return render(request, template, context)
    