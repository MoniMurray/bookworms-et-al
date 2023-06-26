from django.db import models

# Create your models here.


class Signup(models.Model):
    """
    A user signup model to receive Newsletters from Bookworms
    """

    subscribe = models.BooleanField(default=False)
    email = models.OneToOneField(
        "User", on_delete=CASCADE, related_name=newsletter)
    
    def __str__(self):
        """
        Takes in the subscriber's email
        """
        return self.email
