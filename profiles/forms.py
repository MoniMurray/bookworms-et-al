from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'default_address_line1', 
            'default_address_line2',
            'default_town_or_city',
            'default_post_code',
            'default_county_or_state',
            'default_country',
        )

    def __init__(self, *args, **kwargs):

        """Add placeholders and classes, remove auto-generated labels, 
        and set autofocus on first field """

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_address_line1': 'Address Line 1',
            'default_address_line2': 'Address Line 2',
            'default_town_or_city': 'Town or City',
            'default_post_code': 'Postal Code',
            'default_county_or_state': 'County, State or Locality',
        }

        self.fields['default_address_line1'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
                self.fields[field].label = False