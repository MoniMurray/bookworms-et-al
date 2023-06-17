from django.contrib import admin
from .models import Order, OrderLineItem


# Register your models here.
class OrderLineItemAdminInline(admin.TabularInline):
    """ 
    Display the OrderLineItem model fields within the 
    same page as displaying the Order model fields
    """

    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    

class OrderAdmin(admin.ModelAdmin):
    """
    Register the Order model for superuser's Admin use
    """

    inlines = (OrderLineItemAdminInline,)
    # the following fields are calculated by model methods so read-only
    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid',
        'user_profile',
    )
    
    list_display = (
        'order_number',
        'date',
        'full_name',
        'order_total',
        'delivery_cost',
        'grand_total',
    )

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
