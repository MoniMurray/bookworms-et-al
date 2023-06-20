from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """
    listen for webhooks from Stripe
    """

    # setup the Stripe API key and WHSecret to confirm the wh
    # actually came from Stripe
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # THE FOLLOWING IS FROM STRIPE, and then customised

    # Get the webhook data and verify it's signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # invalid payload
        return HttpResponse(content=e, status=400)
    except stripe.error.SignatureVerificationError as e:
        # invalid signature
        return HttpResponse(content=e, status=400)
    except Exception as e:
        # to catch any other exceptions other than the 2 from Stripe above
        return HttpResponse(content=e, status=400)

    # There are over 100 different webhooks from Stripe
    # so passing the event along to a WH Handler in a Class is best
    # as we could even import it into other projects or even OpenSource it.

    # set up a webhook handler
    handler = StripeWH_Handler(request)

    # map webhook events to relevant handler functions
    # in this dictionary, the keys are the wh names coming from Stripe, and
    # the values will be the actual methods inside the handler
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # get the webhook type (key) from Stripe
    event_type = event['type']

    # if there's a handler for it, get it from the event_map or use
    # the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # call the event handler with the event
    response = event_handler(event)
    return response
