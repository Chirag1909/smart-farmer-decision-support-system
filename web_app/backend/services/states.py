import pandas as pd
from ..config import DATA_DIR

RANKING_FILE = DATA_DIR / "best_crop_mandi_ranking.csv"

def get_states():
    """Get unique sorted states from ranking CSV."""
    try:
        df = pd.read_csv(RANKING_FILE)
        states = sorted(df['state'].unique())
        return states
    except FileNotFoundError:
        # Fallback states
        return [
            'Andhra Pradesh', 'Chattisgarh', 'Gujarat', 'Karnataka', 'Kerala', 
            'Madhya Pradesh', 'Maharashtra', 'Odisha', 'Rajasthan', 'Tamil Nadu', 
            'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
        ]

