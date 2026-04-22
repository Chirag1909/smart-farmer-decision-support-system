import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

YIELD_FILE = os.path.join(BASE_DIR, "processed_data", "yield_predictions.csv")
STEP5_FILE = os.path.join(BASE_DIR, "processed_data", "best_crop_mandi_ranking.csv")
STEP6_FILE = os.path.join(BASE_DIR, "processed_data", "best_crop_net_profit_ranking.csv") 