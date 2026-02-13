from django.db import models
from django.utils import timezone

class Account(models.Model):
    OWNER_CHOICES = [
        ('Husband', 'Husband'),
        ('Wife', 'Wife'),
        ('Joint', 'Joint'),
    ]
    name = models.CharField(max_length=50, choices=OWNER_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Budget(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    limit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rollover_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('month', 'year')

    def __str__(self):
        return f"{self.month}/{self.year} - Limit: {self.limit_amount}"

class Transaction(models.Model):
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_unexpected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"
