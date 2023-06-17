from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib import messages


# Create your views here.
@login_required
def profile(request):
    """
    Display the user's profile
    """
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed.  Please ensure the form is valid.')
    else:
        form = ProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)

def order_history(request, order_number):
    """
    Display User's order history
    """

    order = get_object_or_404(Order, order_number=order_number)
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}.'
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        # this variable will be used to check in the checkout_success.html 
        # whether the user got to that template via the order history view
        'from_profile': True,
    }

    return render(request, template, context)