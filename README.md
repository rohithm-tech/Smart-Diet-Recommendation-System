# Smart Diet Recommendation System — NutriOS

AI-powered Indian diet recommendation system built with Django and Random Forest ML.

## Features
- 🧠 Random Forest ML diet prediction (7+ protocols)
- 🇮🇳 5-region Indian cuisine (North, South, Bengali, Gujarati, Marathi)
- ⏱ Intermittent Fasting support (16:8, 5:2, OMAD)
- 💧 Daily water intake tracker
- 📊 BMI progress tracking with Chart.js
- ⚡ Nutrient deficiency alerts
- 📄 PDF diet plan export
- 🎨 Aurora Health glassmorphism UI

## Local Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## Deploy to Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → **Blueprint**
3. Connect your GitHub repo
4. Render auto-reads `render.yaml` and deploys everything

Or manually: New → **Web Service** → Connect repo → set:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn diet_system.wsgi:application`
- Add env vars: `SECRET_KEY`, `DEBUG=False`, `RENDER=True`
