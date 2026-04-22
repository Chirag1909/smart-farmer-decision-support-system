import os
import pandas as pd
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from xgboost import XGBClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "processed_data",
    "crop_model_dataset.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "processed_data",
    "crop_recommendation_model_topk.pkl"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATA_PATH)
print("Dataset loaded successfully")

X = df.drop("crop", axis=1)
y = df["crop"]

# Encode target
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Column groups
categorical_cols = ["soil_type"]
numerical_cols = [c for c in X.columns if c not in categorical_cols]

# ---------------- PREPROCESSOR ----------------
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ]
)

# ---------------- MODEL ----------------
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.08,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="multi:softprob",
    eval_metric="mlogloss",
    random_state=42
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    stratify=y_encoded,
    random_state=42
)

# ---------------- TRAIN ----------------
pipeline.fit(X_train, y_train)

# ---------------- TOP-K EVALUATION ----------------
proba = pipeline.predict_proba(X_test)

def top_k_accuracy(y_true, y_prob, k=3):
    correct = 0
    for i in range(len(y_true)):
        top_k = np.argsort(y_prob[i])[-k:]
        if y_true[i] in top_k:
            correct += 1
    return correct / len(y_true)

top1 = top_k_accuracy(y_test, proba, k=1)
top5 = top_k_accuracy(y_test, proba, k=5)

print(f"\nTop-1 Accuracy : {top1:.4f}")
print(f"Top-5 Accuracy : {top5:.4f}")


# Confusion matrix for reference
y_pred = np.argmax(proba, axis=1)
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ---------------- SAVE MODEL ----------------
joblib.dump(
    {
        "model": pipeline,
        "label_encoder": label_encoder,
        "feature_columns": X.columns.tolist()
    },
    MODEL_PATH
)

print(f"\nTop-K model saved at:\n{MODEL_PATH}")
