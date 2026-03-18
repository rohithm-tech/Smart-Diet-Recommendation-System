import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diet_system.settings')
django.setup()

from recommender.models import FoodItem

foods = [
    {"name": "Apple", "calories": 52, "protein": 0.3, "carbs": 14, "fats": 0.2, "category": "vegan"},
    {"name": "Chicken Breast", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "category": "non_veg"},
    {"name": "Rice (White, Cooked)", "calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3, "category": "vegan"},
    {"name": "Egg (Boiled)", "calories": 155, "protein": 13, "carbs": 1.1, "fats": 11, "category": "non_veg"},
    {"name": "Broccoli", "calories": 34, "protein": 2.8, "carbs": 6.6, "fats": 0.4, "category": "vegan"},
]

for item in foods:
    FoodItem.objects.get_or_create(**item)

print("Food items added!")
