from django.db import models
from django.conf import settings
from products.models import Product
  # Import Product model from your 'products' app

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # The user placing the order
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    # The store manager updating the order status
    store_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_orders'
    )
    # Order status
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    # Order creation date
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Status: {self.status}"


class OrderItem(models.Model):
    # Each order item belongs to a specific order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    # Each order item references a specific product
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    # Number of boxes of the product in the order
    boxes = models.IntegerField()
    # Number of pieces of the product in the order
    pieces = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} in Order {self.order.id}"
