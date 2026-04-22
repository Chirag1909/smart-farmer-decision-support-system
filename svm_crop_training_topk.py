import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# ================== PATH SETUP ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "processed_data",
    "crop_model_dataset.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "processed_data",
    "svm_crop_recommendation_model_topk.pkl"
)

# ================== LOAD DATA ==================
df = pd.read_csv(DATA_PATH)
print("Dataset loaded successfully")

# ================== TARGET ENCODING ==================
label_encoder = LabelEncoder()
df["crop_encoded"] = label_encoder.fit_transform(df["crop"])

# ================== FEATURES / TARGET ==================
X = df.drop(columns=["crop", "crop_encoded"])
y = df["crop_encoded"]

# ================== HANDLE CATEGORICAL ==================
X = pd.get_dummies(X, drop_first=True)

# ================== TRAIN TEST SPLIT ==================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ================== SVM PIPELINE ==================
svm_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        kernel="rbf",
        C=10,
        gamma="scale",
        probability=True,
        random_state=42
    ))
])

# ================== TRAIN MODEL ==================
svm_pipeline.fit(X_train, y_train)

# ================== TOP-1 ACCURACY ==================
y_pred_top1 = svm_pipeline.predict(X_test)
top1_accuracy = accuracy_score(y_test, y_pred_top1)

# ================== TOP-K ACCURACY FUNCTION ==================
def top_k_accuracy(model, X, y_true, k):
    probas = model.predict_proba(X)
    correct = 0

    for i in range(len(y_true)):
        top_k = np.argsort(probas[i])[-k:]
        if y_true.iloc[i] in top_k:
            correct += 1

    return correct / len(y_true)

# ================== TOP-K METRICS ==================
top3_accuracy = top_k_accuracy(svm_pipeline, X_test, y_test, k=3)
top5_accuracy = top_k_accuracy(svm_pipeline, X_test, y_test, k=5)

# ================== RESULTS ==================
print("\nSVM Performance")
print(f"Top-1 Accuracy : {top1_accuracy:.4f}")
print(f"Top-3 Accuracy : {top3_accuracy:.4f}")
print(f"Top-5 Accuracy : {top5_accuracy:.4f}")

# ================== SAVE MODEL ==================
joblib.dump(
    {
        "model": svm_pipeline,
        "label_encoder": label_encoder,
        "feature_columns": X.columns.tolist()
    },
    MODEL_PATH
)

print("\nModel saved successfully at:")
print(MODEL_PATH)
