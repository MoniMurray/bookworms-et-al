from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Author


class ProductForm(forms.ModelForm):
    """
    Store Owner/Admin Product Form to manage Store's product offering
    """

    class Meta:
        """
        This inner metaclass will define the Model and the fields
        to include
        """

        model = Product
        # fields = "__all__"
        fields = ['author', 'name', 'category_name', 'description', 'price', 'type', 'image_url', 'image', 'rating']

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        """
        Override the init() method to make changes to some fields
        """
        super().__init__(*args, **kwargs)


class AuthorForm(forms.ModelForm):
    """
    Store Owner/Admin Product Form to manage Store's product offering
    """

    class Meta:
        """
        This inner metaclass will define the Model and the fields
        to include
        """

        model = Author
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Override the init() method to make changes to some fields
        """
        super().__init__(*args, **kwargs)
