from django.db import models

# Create your models here.


class Signup(models.Model):
    """
    A user signup model to receive Newsletters from Bookworms
    """
    name = models.CharField(max_length=180, null=True, blank=True)
    subscribe = models.BooleanField(default=False)
    email = models.EmailField(
        unique=True, max_length=180, null=False, blank=False)

    class Meta:
        """
        Direct how the admin calls the plural of the Signup model"
        """
        verbose_name_plural = 'Signup'

    def __str__(self):
        """
        Takes in the subscriber's email
        """
        return self.email

