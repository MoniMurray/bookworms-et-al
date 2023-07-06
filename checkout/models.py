from django.db import models
import uuid
from django_countries.fields import CountryField
from django.db.models import Sum
from django.conf import settings
from products.models import Product
from profiles.models import Profile


# Create your models here.
class Order(models.Model):
    """
    A class to create and track orders for anyone who makes a purchase
    """

    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    address_line1 = models.CharField(max_length=80, null=False, blank=False)
    address_line2 = models.CharField(max_length=80, null=False, blank=False)
    county_or_state = models.CharField(max_length=80, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')
    user_profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='orders')

    def _generate_order_number(self):
        """
        Generate a random, unique 32-character order number using uuid
        """

        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already
        """

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def update_total(self):
        """
        A method to update the total by using the Sum() function
        accross all line item total fields for all line items on
        this order
        """

        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.country != 'IE':
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE/100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """ A line item will be like an individual shopping bag item,
    relating to a specific order, and referencing the Product itself """

    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False)

    def save(self, *args, **kwargs):
        """ Multiply the product price by the quantity for each lineitem
        to get the line item total """

        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} on order {self.order.order_number}'
