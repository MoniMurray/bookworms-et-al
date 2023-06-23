from django.db import models

TYPE_CHOICES = [("a", "Hardback"), ("b", "Paperback"), ("c", "Kindle")]


# Create your models here.
class Category(models.Model):
    """
    A model to allocate Categories to the books
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)

    def __str__(self):
        """Takes in the Category model name"""
        return self.name


class Product(models.Model):
    """
    A model to define the book product table
    """

    name = models.CharField(max_length=254, null=False, blank=False)
    category_name = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(
        "Author", null=False, blank=False, on_delete=models.CASCADE
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="Hardback")
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        """
        Takes in the Product name
        """
        return self.name


class Author(models.Model):
    """
    A model to define an author
    """

    name = models.CharField(max_length=254, null=False, blank=False)

    def __str__(self):
        """
        Takes in the Author name
        """
        return self.name
