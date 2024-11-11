from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

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

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_seen = models.BooleanField(default=False)  # Mark as seen/unseen
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - {'Seen' if self.is_seen else 'Unseen'}"