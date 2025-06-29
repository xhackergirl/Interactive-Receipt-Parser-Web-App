from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='receipts/')
    raw_text = models.TextField(blank=True)
    vendor = models.CharField(max_length=255, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor or 'Unknown'} - {self.total or '?'}"