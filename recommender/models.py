from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')

    LIFESTYLE_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('lightly_active', 'Lightly Active'),
        ('moderately_active', 'Moderately Active'),
        ('very_active', 'Very Active'),
    ]
    lifestyle = models.CharField(max_length=20, choices=LIFESTYLE_CHOICES, default='sedentary')

    REGION_CHOICES = [
        ('north', 'North Indian'),
        ('south', 'South Indian'),
        ('bengali', 'Bengali'),
        ('gujarati', 'Gujarati'),
        ('maharashtrian', 'Maharashtrian'),
    ]
    region_preference = models.CharField(max_length=20, choices=REGION_CHOICES, default='north')

    FASTING_CHOICES = [
        ('none', 'No Fasting'),
        ('16_8', 'Intermittent 16:8'),
        ('5_2', 'Intermittent 5:2'),
        ('omad', 'One Meal a Day (OMAD)'),
    ]
    fasting_mode = models.CharField(max_length=10, choices=FASTING_CHOICES, default='none')
    
    # Health conditions
    has_diabetes = models.BooleanField(default=False)
    has_hypertension = models.BooleanField(default=False)
    has_heart_disease = models.BooleanField(default=False)
    has_celiac = models.BooleanField(default=False, verbose_name="Celiac / Gluten Intolerance")
    has_lactose_intolerance = models.BooleanField(default=False, verbose_name="Lactose Intolerance")
    
    target_weight = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.height and self.weight:
            height_m = self.height / 100
            self.bmi = round(self.weight / (height_m * height_m), 2)
        super().save(*args, **kwargs)
        # Auto-log weight history on every save
        if self.weight and self.bmi:
            WeightHistory.objects.create(user=self.user, weight=self.weight, bmi=self.bmi)

    def __str__(self):
        return self.user.username


class WeightHistory(models.Model):
    """Tracks historical BMI & Weight snapshots for real progress charts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_history')
    weight = models.FloatField()
    bmi = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['recorded_at']

    def __str__(self):
        return f"{self.user.username} - {self.bmi} BMI on {self.recorded_at.date()}"


class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField(help_text="Calories per 100g")
    protein = models.FloatField(help_text="Protein in grams per 100g")
    carbs = models.FloatField(help_text="Carbs in grams per 100g")
    fats = models.FloatField(help_text="Fats in grams per 100g")
    
    CATEGORY_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non_veg', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='veg')

    def __str__(self):
        return f"{self.name} ({self.calories} kcal/100g)"

class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    total_daily_calories = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} for {self.user.username}"

class Meal(models.Model):
    diet_plan = models.ForeignKey(DietPlan, related_name='meals', on_delete=models.CASCADE)
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    food_items = models.ManyToManyField(FoodItem)
    
    def __str__(self):
        return f"{self.meal_type} of {self.diet_plan.name}"

class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity_g = models.FloatField(help_text="Quantity in grams")
    
    @property
    def total_calories(self):
        return (self.quantity_g / 100) * self.food_item.calories

    @property
    def total_protein(self):
        return (self.quantity_g / 100) * self.food_item.protein

    @property
    def total_carbs(self):
        return (self.quantity_g / 100) * self.food_item.carbs

    @property
    def total_fats(self):
        return (self.quantity_g / 100) * self.food_item.fats

    def __str__(self):
        return f"{self.user.username} ate {self.quantity_g}g of {self.food_item.name} on {self.date}"
