import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Load dataset
df = pd.read_csv("Ransomware_Data.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)

# 2. Separate features and target
X = df.drop("Ware Type", axis=1)
y = df["Ware Type"]

# 3. Convert labels to numbers
# good = 0, ransom = 1
y = y.map({
    "good": 0,
    "ransom": 1
})

# 4. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# 5. Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

# 6. Train model
print("\nTraining model...")
model.fit(X_train, y_train)

print("Training completed!")

# 7. Make predictions
y_pred = model.predict(X_test)

# 8. Evaluate model
accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL RESULTS")
print("==============================")

print("\nAccuracy:", accuracy)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Benign", "Ransomware"]
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))