import django
from django.core.management import execute_from_command_line
import os
import sys

# Set up Django settings (ensure it points to your project's settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warehouse.settings")
django.setup()

from user.models import User

# Create a list of first names and last names
names = [
    ("Alice", "Johnson"),
    ("Bob", "Smith"),
    ("Charlie", "Davis"),
    ("David", "Taylor"),
    ("Eva", "Anderson"),
    ("Fay", "Martinez"),
    ("George", "Roberts"),
    ("Hannah", "Clark"),
    ("Ivy", "Lewis"),
    ("Jack", "Walker")
]

# Define the store name
store_name = "Luekamia Pharmaceuticals"

# Password for all users
password = "testpassword123"  # You can replace this with a more secure password

# Create 6 users with shop=True and 4 users with store_manager=True
users = []
for i, (first_name, last_name) in enumerate(names):
    if i < 6:
        shop = True
        store_manager = False
    else:
        shop = False
        store_manager = True

    username = f"{first_name.lower()}{last_name.lower()}"
    email = f"{username}@luekamia.com"

    # Create the user
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        store_name=store_name,
        password=password,
        shop=shop,
        store_manager=store_manager
    )
    users.append(user)

    print(f"Created user: {user.username}, Email: {user.email}")
    print(f"Password for authentication: {password}")
