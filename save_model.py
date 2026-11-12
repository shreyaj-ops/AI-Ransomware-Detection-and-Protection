import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("Ransomware_Data.csv")

# Separate features and target
X = df.drop("Ware Type", axis=1)

y = df["Ware Type"].map({
    "good": 0,
    "ransom": 1
})

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

# Train
print("Training model...")
model.fit(X_train, y_train)

print("Training completed!")

# Save model
joblib.dump(model, "ransomware_model.pkl")

# Save feature names
joblib.dump(list(X.columns), "feature_names.pkl")

print("Model saved as ransomware_model.pkl")
print("Feature names saved as feature_names.pkl")