from django import forms
from .models import Signup


class SignupForm(forms.ModelForm):
    """
    A form to subscribe for newsletters
    """

    class Meta:
        model = Signup
        fields = ('name', 'email', 'subscribe',)

   
