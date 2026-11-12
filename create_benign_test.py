import pandas as pd
import joblib

# Load dataset
df = pd.read_csv("Ransomware_Data.csv")

# Load trained model
model = joblib.load("ransomware_model.pkl")
feature_names = joblib.load("feature_names.pkl")

# Select only model features
X = df[feature_names]

# Predict
predictions = model.predict(X)

# Keep samples predicted as benign
benign_data = df[predictions == 0].head(40)

# Remove target column because the Streamlit app doesn't need it
benign_data = benign_data.drop(columns=["Ware Type"])

# Save benign test dataset
benign_data.to_csv(
    "benign_test_samples.csv",
    index=False
)

print("================================")
print("Benign test dataset created!")
print("================================")
print("Samples:", len(benign_data))
print("Saved as: benign_test_samples.csv")