from django.contrib import admin
from .models import Signup


class SignupAdmin(admin.ModelAdmin):
    """
    Display the Signup list in Admin
    """

    list_display = ('name', 'email', 'subscribe')


admin.site.register(Signup)

