from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from bag.contexts import bag_contents
from products.models import Product
from .models import Order, OrderLineItem
from profiles.forms import ProfileForm
from profiles.models import Profile

import stripe

import json


@require_POST
def cache_checkout_data(request):
    """
    Take care of adding the customer's information to My Profile
    if the customer has checked the checkbox
    """

    # before calling the ConfirmCardPayment() method in stripe js,
    # we make a POST request to this view and give it the client secret
    # from the PaymentIntent. Split that at the word _secret and the
    # first part will be the PID

    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be processed.\
        Please try again later'))
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
     Get the shopping bag from the session;
    if there's nothing in the bag return a simple error message
    and redirect back to the products page;
    create an instance of Orderform, which will be empty for now,
    and then create the template, the context containing the Orderform,
    and finally render it all out.
    """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # check whether the method is 'post'
    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'post_code': request.POST['post_code'],
            'town_or_city': request.POST['town_or_city'],
            'address_line1': request.POST['address_line1'],
            'address_line2': request.POST['address_line2'],
            'county_or_state': request.POST['county_or_state'],
        }
        order_form = OrderForm(form_data)

        # if the form is valid, we'll save the order, and then iterate
        # through the bag items to create each line item(similar to
        # context processor code)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, quantity in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(quantity, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )
                        order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database"
                        "Please call us for more information"
                    ))
                    order.delete()
                    return redirect(reverse('view_bag'))
            request.session['save_info'] = 'save_info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, (
                'There was an error with your form.\Please check your information'))
    else:
        bag = request.session.get('bag', {})
        # if nothing in the bag
        if not bag:
            messages.error(
                request, "There is nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)

        # set the secret key on Stripe
        stripe.api_key = stripe_secret_key

        # create the paymentIntent
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        if request.user.is_authenticated:
            # if yes, get their profile and use the 'initial' parameter
            # on the order form to prefill its fields with the relevant info
            try:
                profile = Profile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'post_code': profile.default_post_code,
                    'town_or_city': profile.default_town_or_city,
                    'address_line1': profile.default_address_line1,
                    'address_line2': profile.default_address_line2,
                    'county_or_state': profile.default_county_or_state,
                })
            except Profile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
                request, 
                f'Stripe public key is missing./Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """ Handle successful checkouts """

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # to associate an order with a user's profile,
    # add the user profile to the view
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        # attach the user's profile to their order
        order.user_profile = profile
        order.save()

        # use the data in the save_info checkbox
        if save_info:
            profile_data = {
                'default_full_name': order.full_name,
                'default_email': order.email,
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_post_code': order.post_code,
                'default_town_or_city': order.town_or_city,
                'default_address_line1': order.address_line1,
                'default_address_line2': order.address_line2,
                'default_county_or_state': order.county_or_state,
            }
            user_profile_form = ProfileForm(
                profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed!\
        Your order number is {order_number}.  A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
