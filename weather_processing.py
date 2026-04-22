import pandas as pd
import os
from utils import clean_columns

BASE_PATH = "Weather Dataset"
all_states = []

for root, dirs, files in os.walk(BASE_PATH):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)

            df = pd.read_csv(
                file_path,
                engine="python",
                on_bad_lines="skip"
            )

            df = clean_columns(df)

            # Extract state name from filename
            state_name = file.replace(".csv", "").replace("_", " ").title()

            # Aggregate all numeric weather variables
            numeric_cols = df.select_dtypes(include="number").columns

            if len(numeric_cols) == 0:
                print(f"Skipping {state_name} (no numeric columns)")
                continue

            weather_summary = (
                df[numeric_cols]
                .mean()
                .to_frame()
                .T
            )

            weather_summary["state"] = state_name
            all_states.append(weather_summary)

            print(f"Processed: {state_name}")

# Final check
if not all_states:
    raise RuntimeError("No weather files were processed.")

final_weather = pd.concat(all_states, ignore_index=True)
final_weather.to_csv("processed_data/weather_cleaned.csv", index=False)

print("✅ Weather data processed as state-level climatic features")
