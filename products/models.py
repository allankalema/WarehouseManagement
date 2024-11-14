from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

# Define the Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    manufactured_date = models.DateField()
    expiry_date = models.DateField()
    boxes = models.IntegerField(default=0)  # Number of boxes when the product is created
    pieces_per_box = models.IntegerField(default=0)  # Pieces per box, default to 0 to avoid None
    pieces_left = models.IntegerField()  # Pieces left in total
    boxes_left = models.IntegerField(default=0)  # Boxes left in stock, set default to 0 to avoid null values
    section = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    store_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def calculate_remaining_pieces(self):
        """Calculate the total remaining pieces (pieces_left * boxes_left)."""
        return self.pieces_left * self.boxes_left

    def calculate_remaining_boxes(self):
        """Calculate the total remaining boxes (boxes_left)."""
        return self.boxes_left

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation, not update
            self.boxes_left = self.boxes or 0  # Ensure boxes_left is a non-None integer
            self.pieces_left = (self.pieces_per_box or 0) * self.boxes  # Ensure pieces_left is calculated correctly
        super().save(*args, **kwargs)


# Define the signal receiver function outside the Product model class
@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, **kwargs):
    # Check if boxes_left is 2 or below
    if instance.boxes_left <= 2:
        # Get the User model
        User = get_user_model()

        # Find users with matching store_name and owner or store_manager role
        users_to_notify = User.objects.filter(
            store_name=instance.store_name,
            owner=True,
            store_manager=True
        )

        # Notify and email each user
        for user in users_to_notify:
            # Create notification
            Notification.objects.create(
                user=user,
                message=f"Product '{instance.name}' is low on stock (Boxes Left: {instance.boxes_left})."
            )

            # Send email alert
            send_mail(
                subject="Low Stock Alert",
                message=(
                    f"Dear {user.first_name},\n\n"
                    f"The product '{instance.name}' in your store '{instance.store_name}' "
                    f"is low on stock with only {instance.boxes_left} boxes left.\n"
                    "Please restock soon.\n\nBest,\nInventory System"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )


User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_seen = models.BooleanField(default=False)  # Mark as seen/unseen
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - {'Seen' if self.is_seen else 'Unseen'}"