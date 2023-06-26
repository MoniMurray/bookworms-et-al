from django import forms
from .models import Signup


class SignupForm(forms.ModelForm):
    """
    A form to subscribe for newsletters
    """

    class Meta:
        model = Signup
        fields = ('name', 'email', 'subscribe',)

    def __init__(self, *args, **kwargs):

        """initialise form"""

        super().__init__(*args, **kwargs)
