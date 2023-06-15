from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def profile (request):
    """
    Display the user's profile
    """
    profile = get_object_or_404(Profile, user=request.user)
    template = 'profiles/profile.html'
    context = {
        'profile': profile,

    }

    return render(request, template, context)
    