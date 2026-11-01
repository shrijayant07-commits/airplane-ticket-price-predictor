import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv("dataset/airlines_flights_data.csv")

# Prepare features and target
X = df.drop(["price", "index", "flight"], axis=1)
y = df["price"]

# Encode categorical columns
X = pd.get_dummies(X, dtype=int)

# Train smaller Random Forest
model = RandomForestRegressor(
    n_estimators=30,
    max_depth=15,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

# Save model
joblib.dump(
    {"model": model, "columns": X.columns.tolist()},
    "ticket_price_model.pkl",
    compress=3
)

print("Model training completed!")
print("New model size:", round(
    __import__("os").path.getsize("ticket_price_model.pkl") / (1024**2), 2
), "MB")