from django.db import models


class Company(models.Model):  # Include a field geo data
    name = models.CharField(max_length=255)
    address = models.TextField()
    postcode = models.CharField(max_length=10)
    category = models.CharField(max_length=100)
    allowance = models.DecimalField(max_digits=10, decimal_places=2)
    blacklisted = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
