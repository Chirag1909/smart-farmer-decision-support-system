def get_dashboard_data(state):
    return {
        "top_crops": [
            {"crop": "Groundnut", "yield": 52.6, "price": 9800},
            {"crop": "Maize", "yield": 55.1, "price": 2400}
        ],
        "best_crop": {
            "name": "Groundnut",
            "price": 6639,
            "profit": 270000,
            "margin": 77
        }
    }