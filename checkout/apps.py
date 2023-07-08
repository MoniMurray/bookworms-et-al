from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    Include application configuration in the app
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        """
        Override the ready method by importing signals module,
        updating the order totals automatically
        """
        import checkout.signals
