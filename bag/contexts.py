from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    Instead of returning template, this function will return a dictionary
    called 'context', it's purpose is to make the dictionary available
    to all templates accross the entire application
    """
    bag_items = []
    subtotal = 0
    product_count = 0
    bag = request.session.get('bag', {})

    # iterate through all the items in the shopping bag, and along the way tally up the
    # total cost and product count and add the products and their data to the bag items list.

    for item_id, quantity in bag.items():
        # item data will be an int
        # if isinstance(item_data, int):
        product = get_object_or_404(Product, pk=item_id)
        subtotal += quantity * product.price
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })
            # otherwise, if the item data is a dictionary we know there are sizes
        # else:
        #     product = get_object_or_404(Product, pk=item_id)
        #     for size, quantity in item_data['items_by_size'].items():
        #         subtotal += quantity * product.price
        #         product_count += quantity
        #         bag_items.append({
        #             'item_id': item_id,
        #             'quantity': quantity,
        #             'product': product,
        #             'size': size,
        #         })

    if subtotal < settings.FREE_DELIVERY_THRESHOLD:
        delivery = subtotal * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - subtotal
    else:
        delivery = 0
        free_delivery_delta = 0

    total = delivery + subtotal

    context = {
        'bag_items': bag_items,
        'subtotal': subtotal,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'total': total,
    }

    return context
