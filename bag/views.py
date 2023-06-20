from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from products.models import Product
from django.contrib import messages


# Create your views here.
def view_bag(request):
    """
    A view to return the shopping bag
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add a quantity of the specified product to the shopping bag
    """
    product = get_object_or_404(Product, pk=item_id)

    redirect_url = reverse('products')
    bag = request.session.get('bag', {})
    quantity = 1

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        redirect_url = request.POST.get('redirect_url')

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(
            request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of a specified product to the shopping bag
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))

    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def delete_from_bag(request, item_id):
    """
    delete a product from the shopping bag
    """
    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})

        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error deleting item: {e}')
        return HttpResponse(status=500)
