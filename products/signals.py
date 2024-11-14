# products/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Product, Notification

# The signal to track changes to 'boxes_left' field
@receiver(pre_save, sender=Product)
def track_stock_change(sender, instance, **kwargs):
    # Check if the instance is being updated (not created)
    if instance.pk:
        # Fetch the existing instance from the database
        existing_product = Product.objects.get(pk=instance.pk)

        # Compare the old and new values for boxes_left
        if existing_product.boxes_left != instance.boxes_left:
            # Trigger the low stock check if boxes_left has changed
            if instance.boxes_left <= 2:
                send_low_stock_notifications(instance)

def send_low_stock_notifications(instance):
    """Send notification and email when stock is low."""
    User = get_user_model()
    
    # Find users with matching store_name and roles (owner, store_manager)
    users_to_notify = User.objects.filter(
        store_name=instance.store_name,
        owner=True,
        store_manager=True
    )
    
    # Create notifications and send email to each user
    for user in users_to_notify:
        # Create the notification
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
