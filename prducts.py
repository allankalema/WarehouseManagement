import django
from django.utils import timezone
from datetime import timedelta
import random
import os

# Set up Django settings (ensure it points to your project's settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warehouse.settings")
django.setup()

from products.models import Product  # Replace 'inventory' with your app's name if different

# Define sample medical product names and descriptions
product_data = [
    ("Paracetamol Tablets", "Pain reliever and fever reducer."),
    ("Ibuprofen Capsules", "Anti-inflammatory and pain reliever."),
    ("Amoxicillin Syrup", "Antibiotic for bacterial infections."),
    ("Vitamin C Tablets", "Dietary supplement for immune support."),
    ("Antihistamine Syrup", "Used to treat allergic reactions."),
    ("Cough Syrup", "Used for relief of cough and cold symptoms."),
    ("Insulin Injections", "Hormone injection for diabetes management."),
    ("Antacid Tablets", "Reduces stomach acidity."),
    ("Anti-malarial Tablets", "Medication for malaria treatment."),
    ("Eye Drops", "Used for eye infections and dryness."),
    ("Bandages", "Sterile adhesive bandages for wound care."),
    ("Antibiotic Ointment", "Topical antibiotic for minor wounds."),
    ("Multivitamin Tablets", "Dietary supplement with essential vitamins."),
    ("Pain Relief Gel", "Topical gel for muscle and joint pain."),
    ("Glucose Test Strips", "Used for blood glucose monitoring."),
    ("Saline Nasal Spray", "Moisturizing spray for dry nasal passages."),
    ("Hydrocortisone Cream", "Topical cream for skin irritation."),
    ("Antifungal Cream", "Used for treating fungal infections."),
    ("Blood Pressure Monitor", "Electronic device for BP measurement."),
    ("Thermometer", "Device for measuring body temperature."),
    ("Pregnancy Test Kits", "Used for determining pregnancy."),
    ("Hand Sanitizer", "Antibacterial hand rub."),
    ("Disinfectant Wipes", "Surface disinfectant wipes."),
    ("Face Masks", "Protective face masks."),
    ("IV Drip Kit", "Used for intravenous therapy."),
]

# Define the store name
store_name = "Luekamia Pharmaceuticals"

# Define the current date
current_date = timezone.now()

# Define expiry dates
expiry_dates = [
    current_date + timedelta(days=90),  # 3 months from now
    current_date + timedelta(days=180),  # 6 months from now
    current_date + timedelta(days=730)  # 2 years from now
]

# Create the products
products = []
for i, (name, description) in enumerate(product_data):
    # Randomly set boxes and pieces per box
    boxes = random.randint(1, 20)
    pieces_per_box = random.randint(10, 50)
    
    # Set boxes_left to either low or high
    boxes_left = random.choice([random.randint(1, 5), boxes])

    # Randomly assign an expiry date from the list
    expiry_date = random.choice(expiry_dates)
    
    # Create the product instance
    product = Product(
        name=name,
        description=description,
        manufactured_date=current_date.date(),
        expiry_date=expiry_date.date(),
        boxes=boxes,
        pieces_per_box=pieces_per_box,
        pieces_left=boxes * pieces_per_box,
        boxes_left=boxes_left,
        section="Pharmacy",  # Example section
        store_name=store_name,
        created_at=current_date
    )
    product.save()
    products.append(product)

    print(f"Created product: {product.name}, Boxes Left: {product.boxes_left}, Expiry Date: {product.expiry_date}")

print(f"Total products created: {len(products)}")
