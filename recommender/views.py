from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm, DailyLogForm
from .models import UserProfile, DailyLog, FoodItem, DietPlan, WeightHistory
from .ml_model import predict_diet
from django.contrib import messages
import datetime
import json

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'recommender/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect('profile_setup')
            except Exception:
                messages.error(request, 'That username is already taken. Please try another.')
        else:
            # Surface form validation errors as flash messages
            for field, errors in form.errors.items():
                for error in errors:
                    label = form.fields[field].label or field.replace('_', ' ').title() if field != '__all__' else ''
                    messages.error(request, f'{label}: {error}' if label else error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'recommender/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthenticationForm()
    return render(request, 'recommender/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def profile_setup(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile saved & metrics recalibrated!")
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'recommender/profile_setup.html', {'form': form})

@login_required
def dashboard(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('profile_setup')

    # ── Core AI Prediction ──────────────────────────────────────────────────────
    predicted_diet = predict_diet(
        gender_str=profile.gender,
        age=profile.age,
        bmi=profile.bmi,
        lifestyle_str=profile.lifestyle,
        diab=profile.has_diabetes,
        hyper=profile.has_hypertension,
        heart=profile.has_heart_disease,
        celiac=profile.has_celiac,
        lactose=profile.has_lactose_intolerance
    )
    
    # ── Regional + Fasting-Aware Meal Plan ────────────────────────────────────
    from .diet_generator import generate_meal_plan
    detailed_plan = generate_meal_plan(
        predicted_diet,
        region=profile.region_preference,
        fasting_mode=profile.fasting_mode
    )

    # ── Today's Calorie Logs ──────────────────────────────────────────────────
    today = datetime.date.today()
    logs = DailyLog.objects.filter(user=request.user, date=today)
    total_calories = sum(log.total_calories for log in logs)
    total_protein  = sum(log.total_protein for log in logs)
    total_carbs    = sum(log.total_carbs for log in logs)
    total_fats     = sum(log.total_fats for log in logs)

    # ── Feature 6: Nutrient Deficiency Alerts ────────────────────────────────
    # Target baseline values (adjustable per diet type)
    protein_target = 55 if profile.gender == 'male' else 46
    if predicted_diet and 'High Protein' in predicted_diet:
        protein_target = 120

    nutrient_alerts = []
    if logs.exists():
        if total_protein < protein_target * 0.6:
            nutrient_alerts.append({
                'type': 'warn',
                'nutrient': 'Protein',
                'message': f'Low protein intake ({total_protein:.0f}g). Add Rajma, Paneer, Eggs, or Soya Chunks.',
            })
        if total_carbs > 300:
            nutrient_alerts.append({
                'type': 'crit',
                'nutrient': 'Carbs',
                'message': f'High carb load ({total_carbs:.0f}g). Consider swapping rice for ragi or jowar.',
            })
        if total_fats > 80:
            nutrient_alerts.append({
                'type': 'crit',
                'nutrient': 'Fats',
                'message': f'Excess fat intake ({total_fats:.0f}g). Reduce fried items and ghee.',
            })
    
    # ── Feature 1: Real BMI History ──────────────────────────────────────────
    history_qs = WeightHistory.objects.filter(user=request.user).order_by('recorded_at')[:10]
    bmi_labels  = [h.recorded_at.strftime('%b %d') for h in history_qs]
    bmi_values  = [h.bmi for h in history_qs]
    # Ensure we have at least 2 data points for the chart
    if len(bmi_values) < 2:
        bmi_labels = ['Start', 'Now']
        bmi_values = [round((profile.bmi or 22) + 0.5, 1), profile.bmi or 22]

    form = DailyLogForm()
    
    context = {
        'profile':         profile,
        'predicted_diet':  predicted_diet,
        'detailed_plan':   detailed_plan,
        'logs':            logs,
        'total_calories':  total_calories,
        'total_protein':   total_protein,
        'total_carbs':     total_carbs,
        'total_fats':      total_fats,
        'nutrient_alerts': nutrient_alerts,
        'bmi_labels':      json.dumps(bmi_labels),
        'bmi_values':      json.dumps(bmi_values),
        'form':            form,
    }
    return render(request, 'recommender/dashboard.html', context)

@login_required
def log_food(request):
    if request.method == 'POST':
        form = DailyLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, "Food logged successfully!")
            return redirect('dashboard')
    return redirect('dashboard')

@login_required
def export_plan_pdf(request):
    """Feature 5: Export the user's diet plan as a PDF file."""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('profile_setup')

    predicted_diet = predict_diet(
        gender_str=profile.gender,
        age=profile.age,
        bmi=profile.bmi,
        lifestyle_str=profile.lifestyle,
        diab=profile.has_diabetes,
        hyper=profile.has_hypertension,
        heart=profile.has_heart_disease,
        celiac=profile.has_celiac,
        lactose=profile.has_lactose_intolerance
    )
    from .diet_generator import generate_meal_plan
    detailed_plan = generate_meal_plan(
        predicted_diet,
        region=profile.region_preference,
        fasting_mode=profile.fasting_mode
    )

    # Build a flat grocery list from all meal items
    all_items_text = ' '.join(
        item.lower()
        for items in detailed_plan.values()
        for item in items
    )
    keywords = ['chilla', 'poha', 'dal', 'paneer', 'roti', 'idli', 'dosa', 'rice',
                'curd', 'almonds', 'walnuts', 'peanuts', 'makhana', 'eggs', 'chicken',
                'soya', 'rajma', 'tofu', 'bhindi', 'karela', 'lauki', 'spinach',
                'besan', 'jowar', 'bajra', 'fish', 'methi', 'ragi', 'oats', 'sambar',
                'banana', 'buttermilk']
    grocery_items = sorted(set(
        kw.capitalize() for kw in keywords if kw in all_items_text
    )) + ['Ghee', 'Turmeric', 'Cumin Seeds', 'Mustard Seeds', 'Curry Leaves', 'Salt']

    ctx = {
        'user': request.user,
        'profile': profile,
        'predicted_diet': predicted_diet,
        'detailed_plan': detailed_plan,
        'grocery_items': grocery_items,
        'today_date': datetime.date.today().strftime('%B %d, %Y'),
    }

    from django.template.loader import get_template
    from django.http import HttpResponse
    try:
        from xhtml2pdf import pisa
        template = get_template('recommender/diet_plan_pdf.html')
        html = template.render(ctx, request)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="diet_plan_{request.user.username}.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response
    except ImportError:
        # Fallback: render nice HTML for printing if xhtml2pdf unavailable
        return render(request, 'recommender/diet_plan_pdf.html', ctx)

