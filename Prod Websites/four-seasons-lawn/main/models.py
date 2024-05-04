from django.db import models


class Payment(models.Model):
    """Represents a successful payment"""
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(verbose_name="Created at (UTC)")
    stripe_charge_id = models.CharField(max_length=256)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Return a string representation of model object"""
        return f"{self.email} - ({self.amount}$)."
