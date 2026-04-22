import pandas as pd
import os


def find_dataset(root_dir, filename):
    """
    Recursively search for the dataset file inside project directory
    """
    for root, dirs, files in os.walk(root_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None


def clean_mandi_data(input_file, output_file):
    print("Loading dataset...")
    print(f"Reading from: {input_file}")

    df = pd.read_csv(input_file)

    print(f"Initial shape: {df.shape}")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename for ML consistency
    df.rename(columns={
        "district name": "district",
        "market name": "market",
        "commodity": "crop",
        "price date": "date"
    }, inplace=True)

    # Drop critical missing values
    df.dropna(subset=["state", "district", "market", "crop", "modal_price", "date"], inplace=True)

    # Type conversions
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["modal_price"] = pd.to_numeric(df["modal_price"], errors="coerce")

    df = df[df["modal_price"] > 0]

    print(f"Cleaned shape: {df.shape}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"Cleaned data saved to: {output_file}")


if __name__ == "__main__":

    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DATASET_NAME = "Agriculture_price_dataset.csv"

    INPUT_FILE = find_dataset(PROJECT_ROOT, DATASET_NAME)

    if INPUT_FILE is None:
        raise FileNotFoundError(
            f"{DATASET_NAME} not found anywhere inside project directory"
        )

    OUTPUT_FILE = os.path.join(
        PROJECT_ROOT,
        "processed_data",
        "cleaned_mandi_prices.csv"
    )

    clean_mandi_data(INPUT_FILE, OUTPUT_FILE)
