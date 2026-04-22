<<<<<<< HEAD
# Smart Farmer Decision Support System

Modern Flask dashboard for crop recommendation, yield/profit analytics, mandi price intelligence, and weather insights.

## Features

- JWT-based auth (`/register`, `/login`) with SQLite user store
- State-based crop recommendation using real processed datasets
- Profit analytics dashboard (KPI cards + charts + ranked tables)
- Mandi market analytics (top markets, crop-price comparison, trend charts)
- Weather section with current + 7-day rainfall/temperature forecast
- Fully responsive UI (mobile, tablet, desktop), collapsible sidebar, dark/light mode

## Project Structure

```text
application/
  app.py
  templates/
  static/
  routes/
  models/
  services/
  database/
```

## Data Sources Used

- `processed_data/best_crop_mandi_ranking.csv`
- `processed_data/cleaned_mandi_prices.csv`
- `processed_data/best_crop_net_profit_ranking.csv`
- `processed_data/weather_cleaned.csv`

## Run Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create env file:
   ```bash
   copy .env.example .env
   ```
3. Set your OpenWeather key in `.env`:
   - `OPENWEATHER_API_KEY=...`
4. Run app:
   ```bash
   python app.py
   ```
5. Open: `http://127.0.0.1:10000`

## Deployment (Render / Railway)

This repository is deployment-ready with:

- `Procfile` using gunicorn
- `render.yaml` service config
- `PORT` environment binding
- env-var based weather key loading

### Start command

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

### Required environment variables

- `OPENWEATHER_API_KEY`
- `APP_SECRET_KEY` (recommended)
- `JWT_SECRET_KEY` (recommended)
- `PORT` (provided by Render/Railway automatically)

=======
🌾 Smart Farmer Decision Support System

An AI-powered web application that helps farmers make data-driven decisions using crop recommendation, yield prediction, profit forecasting, mandi price analysis, and real-time weather insights.

📌 Project Overview

Agriculture is highly dependent on environmental conditions, market prices, and crop selection. This system provides an intelligent platform that assists farmers by analyzing data and generating recommendations to maximize profit and productivity.

🎯 Features

🔐 User Authentication (Login & Register)

📍 Location-Based Crop Recommendation

🌱 Yield Prediction using Machine Learning

💰 Profit Forecasting

🏆 Crop Ranking (Top-K Recommendations)

🏬 Mandi Price Comparison

🌦 Real-Time Weather Integration

📊 Interactive Dashboard with Graphs

🕒 Historical Data Tracking


🧠 Machine Learning Models

The system uses multiple ML models:

K-Nearest Neighbors (KNN) → Crop Recommendation

Random Forest → Yield Prediction

Regression Models → Price Forecasting

Time Series Analysis → Mandi Price Trends


🏗 Tech Stack

Frontend

HTML, CSS, JavaScript

Responsive Dashboard UI


Backend

Python Flask


Database

SQLite


Libraries

Pandas

NumPy

Scikit-learn

Matplotlib / Plotly

Requests


APIs

OpenWeather API

📁 Project Structure

hydrology_crop_decision_support/

application/
  app.py
  routes/
  models/
  templates/
  static/
  database/

processed_data/
  best_crop_mandi_ranking.csv
  cleaned_mandi_prices.csv

requirements.txt
README.md
run.py

⚙️ Installation & Setup

1. Clone the Repository

git clone https://github.com/your-username/smart-farmer-decision-support-system.git
cd smart-farmer-decision-support-system

2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Set Environment Variables

Create a .env file:

OPENWEATHER_API_KEY=your_api_key_here

5. Run the Application

python run.py

OR

python application/app.py

🌐 Deployment (Render)

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn application.app:app

📊 Screenshots (Optional)

Add screenshots in a folder named screenshots:

dashboard.png
profit.png
market.png

🧪 Test Cases Covered

✔ User Registration & Login
✔ Crop Recommendation
✔ Yield Prediction
✔ Profit Calculation
✔ Crop Ranking
✔ Historical Data Storage
✔ Mandi Price Comparison

🚀 Future Enhancements

Mobile App Integration

Multi-language Support

IoT Sensor Integration

Advanced AI Models

Smart Alerts for Farmers

👨‍💻 Author

Chirag Khodiyar


⭐ Support

If you like this project, give it a ⭐ on GitHub!
>>>>>>> f0548c8010e1a3a253143b5c780dfbbae5d256b3
