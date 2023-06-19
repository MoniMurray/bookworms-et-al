from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


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
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        """
        Override the init() method to make changes to some fields
        """
        super().__init__(*args, **kwargs)
        # categories = Category.objects.all()
        # names = [(c.id, c.get_name()) for c in categories]

        # self.fields['category'].choices = names
        # for field_name, field in self.fields.items():
        #     field.widget.attrs['class'] = 'border-black rounded-0'