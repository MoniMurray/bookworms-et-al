from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def profile (request):
    """
    Display the user's profile
    """

    template = 'profiles/profile.html'
    context = {

    }

    return render(request, template, context)
    