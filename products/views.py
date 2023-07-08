from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Author
from .forms import ProductForm


def all_products(request):
    """A view to show all products, including sorting and search queries"""

    products = Product.objects.all()
    query = None
    categories = None
    author = None
    sort = None
    direction = None

    # If the Search function is used, search through all the products
    if request.GET:
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("name"))
            if sortkey == "category":
                sortkey = "category_name__name"

            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == "desc":
                    sortkey = f"-{sortkey}"
            products = products.order_by(sortkey)

    # check if Category exists, split it into a list at the commas, use
    # the list to filter the queryset of all products down to 
    # matching products
    if 'category' in request.GET:
        categories = request.GET['category'].split(',')
        products = products.filter(category_name__name__in=categories)
        categories = Category.objects.filter(name__in=categories)

    if 'q' in request.GET:
        query = request.GET['q']

        if not query:
            messages.error(
                request, 'You did not enter any search criteria')
            return redirect(reverse('products'))

        queries = Q(name__icontains=query) | Q(
            description__icontains=query) | Q(
                author__name__icontains=query) | Q(
                    category_name__name__icontains=query
                )

        products = products.filter(queries)

    current_sorting = f"{sort}_{direction}"

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_author": author,
        "current_sorting": current_sorting,
    }

    return render(request, "products/products.html", context)


def get_queryset(self, **kwargs):
    """
    Search product listing
    """

    query = self.request.GET.get("q")
    if query:
        products = self.model.objects.filter(
            Q(name__icontains=query)
            | Q(author__name__icontains=query)
            | Q(category_name__name__icontains=query)
        )
    else:
        products = self.model.objects.all()
    return products


def product_detail(request, product_id):
    """A view to show a product's details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)


@login_required
def add_product(request):
    """
    Add a Product to the store
    """

    # restrict this view function to superusers/store owner
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    if request.method == "POST":
        # instantiate a new instance of the ProductForm from request.POST,
        # include request.Files to allow for images to be captured
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added a Product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request, "Failed to add product. \
                    Please check the form is valid."
            )
    else:
        form = ProductForm()
    template = "products/add_product.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    Edit a Product in the store
    """
    # restrict this view function to superusers/store owner
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    # pre-fill the form wiht the product details
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        # instantiate a new instance of the ProductForm from request.POST,
        # include request.Files to allow for images to be captured, and
        # tell it the specific instance to update is the 'product'
        # obtained above.
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited a Product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request, "Failed to update product. \
                    Please check the form is valid."
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You are editing {product.name}")
    template = "products/edit_product.html"
    context = {
        "form": form,
        "product": product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    Delete a Product from the store
    """
    # restrict this view function to superusers/store owner
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    # pre-fill the form with the product details
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f"{product.name} deleted from the store")

    return redirect(reverse("products"))
