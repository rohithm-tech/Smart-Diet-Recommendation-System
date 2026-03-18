"""
Indian Diet Generator - Localized, Regional, Fasting-Aware
Generates full meal plans based on ML predictions, user region, and fasting mode.
"""

# ── Regional Meal Libraries ────────────────────────────────────────────────────

NORTH_INDIAN = {
    'Diabetic Friendly': {
        'Breakfast': ['Moong Dal Chilla with Green Chutney', 'Methi Paratha (No oil/ghee) with Low-Fat Curd'],
        'Lunch':     ['Multigrain Roti with Karela Sabzi', 'Brown Rice with Toor Dal & Cucumber Raita'],
        'Dinner':    ['Lauki Sabzi with Jowar Roti', 'Palak Dal with Bajra Roti'],
        'Snacks':    ['Roasted Makhana', 'Sprouted Moong Chaat'],
    },
    'DASH / Heart Healthy Diet': {
        'Breakfast': ['Oats Porridge with Almonds & Apple', 'Vegetable Upma (Low Salt)'],
        'Lunch':     ['Whole Wheat Roti with Mixed Dal', 'Bhindi Masala with Curd'],
        'Dinner':    ['Grilled Paneer with Mint Chutney', 'Lauki Curry with Roti'],
        'Snacks':    ['Fresh Papaya & Guava Bowl', 'Unsalted Walnuts'],
    },
    'Weight Loss / Calorie Deficit Diet': {
        'Breakfast': ['Oats Idli with Sambar', 'Poha with Peanuts & Veggies'],
        'Lunch':     ['Ragi Roti with Cabbage Sabzi', 'Dal Tadka with Small Brown Rice'],
        'Dinner':    ['Clear Vegetable Soup', 'Grilled Soya Chunks Salad'],
        'Snacks':    ['Roasted Chana', 'Buttermilk (Chaas)'],
    },
    'High Protein Athlete Diet': {
        'Breakfast': ['Paneer Bhurji with Multigrain Toast', 'Besan Chilla with Paneer Filling'],
        'Lunch':     ['Soya Chunks Curry with Roti', 'Rajma Masala with Quinoa'],
        'Dinner':    ['Tandoori Paneer Tikka', 'Sprouted Moong Dal Khichdi'],
        'Snacks':    ['Boiled Eggs / Protein Shake', 'Roasted Peanuts'],
    },
    'Mediterranean Balanced Diet': {
        'Breakfast': ['Poha with Veggies', 'Idli with Sambar & Coconut Chutney'],
        'Lunch':     ['Whole Wheat Roti with Dal Makhani', 'Mix Veg Sabzi'],
        'Dinner':    ['Jeera Rice with Chana Masala', 'Baingan Bharta with Roti'],
        'Snacks':    ['Mixed Nuts', 'Seasonal Fruit'],
    },
}

SOUTH_INDIAN = {
    'Diabetic Friendly': {
        'Breakfast': ['Ragi Dosa with Coconut Chutney', 'Oats Upma with Curry Leaves'],
        'Lunch':     ['Brown Rice with Sambar & Thoran', 'Ragi Mudde with Palak Curry'],
        'Dinner':    ['Moong Dal Khichdi with Curd', 'Steamed Idli with Karela Sambar'],
        'Snacks':    ['Roasted Chana', 'Buttermilk with Ginger'],
    },
    'DASH / Heart Healthy Diet': {
        'Breakfast': ['Plain Idli with Low-Na Sambar', 'Rava Upma with Vegetables'],
        'Lunch':     ['Steamed Rice with Rasam & Greens', 'Moringa Leaves Dal with Roti'],
        'Dinner':    ['Grilled Fish / Tofu in Coconut Gravy', 'Vegetable Stew with Appam'],
        'Snacks':    ['Banana', 'Coconut Water'],
    },
    'Weight Loss / Calorie Deficit Diet': {
        'Breakfast': ['Oats Idli with Sambar', 'Ragi Porridge with Seeds'],
        'Lunch':     ['Kootu (Lentil Curry) with Steamed Rice', 'Rasam with Boiled Veggies'],
        'Dinner':    ['Clear Rasam', 'Steamed Curd Rice (small portion)'],
        'Snacks':    ['Puffed Rice Chaat', 'Amla Juice'],
    },
    'High Protein Athlete Diet': {
        'Breakfast': ['Egg Dosa / Paneer Dosa', 'Pesarattu (Moong Dal Crepe)'],
        'Lunch':     ['Chicken Chettinad / Soya Chunks Curry with Rice', 'Rajma with Millet Roti'],
        'Dinner':    ['Grilled Prawns / Tofu Curry with Quinoa', 'Protein-Rich Sambar with Idli'],
        'Snacks':    ['Peanut Chikki', 'Roasted Gram'],
    },
    'Mediterranean Balanced Diet': {
        'Breakfast': ['Masala Dosa', 'Idli with Sambar & Gunpowder'],
        'Lunch':     ['Bisi Bele Bath', 'Curd Rice with Pickle'],
        'Dinner':    ['Appam with Vegetable Stew', 'Rava Idli with Chutney'],
        'Snacks':    ['Murukku (baked)', 'Tender Coconut'],
    },
}

BENGALI = {
    'Diabetic Friendly': {
        'Breakfast': ['Moong Dal Chilla with Kalo Jeere', 'Oats Khichuri'],
        'Lunch':     ['Steamed Rice with Shukto & Dal', 'Roti with Bitter Gourd Stir Fry'],
        'Dinner':    ['Moong Dal with Drumstick', 'Fish Curry (low oil) with Brown Rice'],
        'Snacks':    ['Muri (Puffed Rice) with Cucumber', 'Buttermilk'],
    },
    'DASH / Heart Healthy Diet': {
        'Breakfast': ['Poha with Mustard Seeds', 'Oats with Banana'],
        'Lunch':     ['Steamed Rice with Lentil Dal & Vegetables', 'Roti with Begun Bhaja (low oil)'],
        'Dinner':    ['Macher Jhol (Low oil Fish Curry) with Rice', 'Cholar Dal with Roti'],
        'Snacks':    ['Fruits (Guava / Papaya)', 'Chatu (Sattu) Sherbet'],
    },
    'Weight Loss / Calorie Deficit Diet': {
        'Breakfast': ['Muri with Veggies', 'Oats Porridge'],
        'Lunch':     ['Moong Dal with Steamed Rice', 'Sukta & Lentil Soup'],
        'Dinner':    ['Clear Vegetable Soup', 'Curd with Muri'],
        'Snacks':    ['Roasted Chana', 'Amla'],
    },
    'High Protein Athlete Diet': {
        'Breakfast': ['Egg Roll (Whole Wheat)', 'Chatu (Sattu) Shake with Milk'],
        'Lunch':     ['Machher Jhol with Rice', 'Mutton / Soya Curry with Roti'],
        'Dinner':    ['Dimer Dalna (Egg Curry) with Roti', 'Grilled Bhetki with Salad'],
        'Snacks':    ['Boiled Eggs', 'Peanuts'],
    },
    'Mediterranean Balanced Diet': {
        'Breakfast': ['Luchi with Cholar Dal (small portion)', 'Roti with Begun Bharta'],
        'Lunch':     ['Rice, Dal & Macher Jhol', 'Khichuri with Papad'],
        'Dinner':    ['Roti with Aloo Posto', 'Curd Rice'],
        'Snacks':    ['Mishti Doi (small)', 'Seasonal Fruits'],
    },
}

GUJARATI = {
    'Diabetic Friendly': {
        'Breakfast': ['Methi Thepla with Curd', 'Moong Sprout Dhokla'],
        'Lunch':     ['Bajra Roti with Karela Shaak', 'Jowar Roti with Dudhi Muthia'],
        'Dinner':    ['Moong Dal Khichdi with Kadhi', 'Jowar Khichdi with Veggies'],
        'Snacks':    ['Roasted Chana & Peanuts', 'Buttermilk'],
    },
    'DASH / Heart Healthy Diet': {
        'Breakfast': ['Oats Handvo', 'Plain Khakhra with Chutney'],
        'Lunch':     ['Bajra Roti with Ringan Bataka Shaak', 'Dal Dhokli (low salt)'],
        'Dinner':    ['Moong Dal Khichdi with Low-Na Kadhi', 'Vegetable Daliya'],
        'Snacks':    ['Roasted Makhana', 'Fruits'],
    },
    'Weight Loss / Calorie Deficit Diet': {
        'Breakfast': ['Plain Khakhra with Green Chutney', 'Oats Porridge with Seeds'],
        'Lunch':     ['Moong Khichdi', 'Fada Ni Khichdi with Curd'],
        'Dinner':    ['Clear Soup', 'Steamed Dhokla with Chutney'],
        'Snacks':    ['Chaas (Buttermilk)', 'Roasted Chana'],
    },
    'High Protein Athlete Diet': {
        'Breakfast': ['Moong Sprout Dhokla', 'Besan Chilla with Paneer'],
        'Lunch':     ['Rajma with Bajra Roti', 'Soya Chunks Shaak with Roti'],
        'Dinner':    ['Paneer Tikka with Salad', 'Moong Dal Khichdi with Curd'],
        'Snacks':    ['Roasted Peanuts', 'Protein Shake'],
    },
    'Mediterranean Balanced Diet': {
        'Breakfast': ['Thepla with Chutney', 'Handvo Slice with Dahi'],
        'Lunch':     ['Gujarati Dal with Rice & Shaak', 'Undhiyu with Puri (small)'],
        'Dinner':    ['Khichdi with Kadhi', 'Dal Dhokli'],
        'Snacks':    ['Ganthia (baked)', 'Seasonal Fruit'],
    },
}

MAHARASHTRIAN = {
    'Diabetic Friendly': {
        'Breakfast': ['Jowar Bhakri with Pithla', 'Oats Upma with Curry Leaves'],
        'Lunch':     ['Jowar Bhakri with Methi Sabzi', 'Brown Rice with Amti Dal'],
        'Dinner':    ['Ragi Bhakri with Palak Zunka', 'Moong Dal with Bhakri'],
        'Snacks':    ['Roasted Chana', 'Taak (Buttermilk)'],
    },
    'DASH / Heart Healthy Diet': {
        'Breakfast': ['Sabudana Khichdi (small portion)', 'Poha with Peanuts'],
        'Lunch':     ['Bhakri with Bharli Vaangi', 'Roti with Varan Bhaat'],
        'Dinner':    ['Solkadhi with Steamed Rice', 'Boiled Toor Dal with Bhakri'],
        'Snacks':    ['Kokum Sherbet', 'Fruits'],
    },
    'Weight Loss / Calorie Deficit Diet': {
        'Breakfast': ['Poha (No Potato)', 'Oats Upma'],
        'Lunch':     ['Jowar Bhakri with Leafy Sabzi', 'Brown Rice Khichdi'],
        'Dinner':    ['Clear Varan Soup', 'Thalipeeth with Curd'],
        'Snacks':    ['Taak (Buttermilk)', 'Chana Chaat'],
    },
    'High Protein Athlete Diet': {
        'Breakfast': ['Egg Bhurji with Multigrain Roti', 'Thalipeeth with Curd'],
        'Lunch':     ['Chicken Curry / Soya with Bhakri', 'Chana Usal with Rice'],
        'Dinner':    ['Mutton Kolhapuri / Paneer Tikka Masala with Roti', 'Rajma with Bhakri'],
        'Snacks':    ['Roasted Groundnuts', 'Protein Shake'],
    },
    'Mediterranean Balanced Diet': {
        'Breakfast': ['Poha with Lemon', 'Rava Upma with Vegetables'],
        'Lunch':     ['Bhakri with Pithla & Bhaaji', 'Varan Bhaat with Toop (Ghee)'],
        'Dinner':    ['Puran Poli (small)', 'Khichdi with Mattha'],
        'Snacks':    ['Chakli (baked)', 'Kokum Sherbet'],
    },
}

REGIONAL_MAP = {
    'north':         NORTH_INDIAN,
    'south':         SOUTH_INDIAN,
    'bengali':       BENGALI,
    'gujarati':      GUJARATI,
    'maharashtrian': MAHARASHTRIAN,
}

# ── Gluten / Lactose modifiers ─────────────────────────────────────────────────

def _apply_gluten_free(plan):
    substitutions = {
        'Roti':       'Jowar Roti',
        'Bhakri':     'Jowar Bhakri',
        'Toast':      'Gluten-Free Toast',
        'Oats':       'Gluten-Free Oats',
        'Wheat':      'Gluten-Free',
        'Multigrain': 'Gluten-Free Multigrain',
    }
    for meal in plan:
        plan[meal] = [
            ' '.join(substitutions.get(w, w) for w in item.split())
            for item in plan[meal]
        ]
    return plan

def _apply_lactose_free(plan):
    substitutions = {
        'Curd':    'Vegan Yogurt',
        'Paneer':  'Tofu',
        'Dahi':    'Vegan Dahi',
        'Ghee':    'Olive Oil',
        'Milk':    'Oat Milk',
        'Kadhi':   'Vegan Kadhi',
        'Taak':    'Lemon Water',
    }
    for meal in plan:
        plan[meal] = [
            ' '.join(substitutions.get(w.rstrip('.,'), w) + ('.' if w.endswith('.') else '') for w in item.split())
            for item in plan[meal]
        ]
    return plan

# ── Fasting Mode Filter ────────────────────────────────────────────────────────

def _apply_fasting(plan, fasting_mode):
    if fasting_mode == '16_8':
        # Eating window: 12pm – 8pm → only Lunch, Dinner, and a light Snack
        return {k: v for k, v in plan.items() if k in ['Lunch', 'Dinner', 'Snacks']}
    elif fasting_mode == 'omad':
        # One Meal a Day: just a big Lunch
        return {'Lunch (Your One Meal)': plan.get('Lunch', []) + plan.get('Dinner', [])}
    elif fasting_mode == '5_2':
        # On fast days: low-cal meals only (keep snacks + a light dinner)
        return {
            'Permitted Meal (Fast Day)': plan.get('Snacks', []),
            'Light Dinner (Fast Day)':   plan.get('Dinner', []),
        }
    return plan  # no fasting

# ── Main Entry Point ───────────────────────────────────────────────────────────

def generate_meal_plan(prediction_string, region='north', fasting_mode='none'):
    """
    Generates a detailed daily meal plan:
    - Based on the ML prediction string
    - Localized by Indian region
    - Adjusted for dietary intolerances and fasting mode
    """
    regional_library = REGIONAL_MAP.get(region, NORTH_INDIAN)

    # Match the best diet in the library
    plan = None
    for key in regional_library:
        if key.lower() in prediction_string.lower() or prediction_string.lower() in key.lower():
            plan = {k: list(v) for k, v in regional_library[key].items()}
            break

    if plan is None:
        # Fallback: balanced diet
        plan = {k: list(v) for k, v in regional_library['Mediterranean Balanced Diet'].items()}

    # Apply intolerances
    if 'Gluten-Free' in prediction_string:
        plan = _apply_gluten_free(plan)
    if 'Lactose-Free' in prediction_string:
        plan = _apply_lactose_free(plan)

    # Apply fasting mode filter
    plan = _apply_fasting(plan, fasting_mode)

    return plan
