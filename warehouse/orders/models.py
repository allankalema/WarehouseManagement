from django.db import models
from django.conf import settings
from products.models import Product
from user.models import User

# Order model (finalized version of cart)
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

    def total_price(self):
        """Calculate total price for the order based on items and their quantities."""
        return sum(item.get_item_total() for item in self.items.all())

# Cart model (temporary, where user selects products)
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the cart was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the cart was last updated
    status = models.CharField(max_length=20, default='pending', choices=[('pending', 'Pending'), ('completed', 'Completed'), ('abandoned', 'Abandoned')])

    def __str__(self):
        return f"Cart for {self.user.username} ({self.status})"

    def total_price(self):
        """Calculate the total price of the cart based on cart items."""
        return sum(item.get_item_total() for item in self.cart_items.all())

    def get_item_count(self):
        """Get the total number of items in the cart."""
        return self.cart_items.count()

# CartItem model (individual product entries in a cart)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)  # How many of the product the user wants to add

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart"

    def get_item_total(self):
        """Get the total price for this item based on quantity and product price."""
        return self.product.price * self.quantity

    def update_quantity(self, quantity):
        """Update quantity of the product in the cart."""
        self.quantity = quantity
        self.save()

# OrderItem model (individual product entries in an order)
class OrderItem(models.Model):
    # Each order item belongs to a specific order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # Each order item references a specific product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Number of boxes of the product in the order
    boxes = models.IntegerField()
    # Number of pieces of the product in the order
    pieces = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} in Order {self.order.id}"

    def get_item_total(self):
        """Get the total price for this item based on quantity and product price."""
        return self.product.price * self.pieces

    def update_order_item(self, pieces, boxes):
        """Update the order item with new pieces and boxes."""
        self.pieces = pieces
        self.boxes = boxes
        self.save()

# Optional: To make sure Cart converts to Order
def create_order_from_cart(cart):
    """Convert a Cart into an Order."""
    order = Order.objects.create(user=cart.user, status='pending')
    
    for cart_item in cart.cart_items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            pieces=cart_item.quantity,  # Assuming quantity represents pieces
            boxes=cart_item.quantity // cart_item.product.pieces_per_box  # If pieces_per_box is defined in Product
        )
    
    cart.status = 'completed'  # Cart is now completed when converted to an order
    cart.save()
    return order
