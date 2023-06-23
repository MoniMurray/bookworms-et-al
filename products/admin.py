from django.contrib import admin
from .models import Product, Category, Author


class CategoryAdmin(admin.ModelAdmin):
    """
    Display the Category model fields in the Admin view
    """

    list_display = ("name",)


class ProductAdmin(admin.ModelAdmin):
    """
    Display the Product model fields in the Admin view
    """

    list_display = (
        "name",
        "rating",
        "description",
        "price",
        "type",
        "author",
        "image_url",
        "image",
    )

    ordering = ("-rating",)


class AuthorAdmin(admin.ModelAdmin):
    """
    Display the Author model fields in the Admin view
    """

    list_display = ("name",)


admin.site.register(Product, ProductAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Author, AuthorAdmin)
