# products/models.py
from django.db import models
from django.conf import settings  # Import to reference the user model

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    manufactured_date = models.DateField()
    expiry_date = models.DateField()
    boxes = models.IntegerField()  # Moved this field to be before pieces_per_box
    pieces_per_box = models.IntegerField()  # Moved this field to after boxes
    pieces_left = models.IntegerField()  # Left unchanged
    boxes_left = models.IntegerField(blank=True, null=True)  # Can be empty initially
    section = models.CharField(max_length=255, blank=True, null=True)  # Added section field
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    def calculate_remaining_pieces(self):
        """Calculate the total remaining pieces (pieces_left * boxes_left)."""
        return self.pieces_left * self.boxes_left

    def calculate_remaining_boxes(self):
        """Calculate the total remaining boxes (boxes_left)."""
        return self.boxes_left
