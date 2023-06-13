from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):

    summernote_fields = ('content',)
    list_display = (
        'pk',
        'user',
        'bio',
        'image' 
    )


admin.site.register(Profile, ProfileAdmin)
