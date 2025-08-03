import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
df = pd.read_csv("data/processed/music_data.csv")

features = ["session_length", "time_on_track", "track_duration", "energy", "tempo", "repeat_count"]
target = "skipped"
X = df[features]
y = df[target]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

os.makedirs("model", exist_ok=True)
joblib.dump((model, scaler, features), "model/music_boost_model.pkl")

print("✅ Gradient Boosting model trained and saved.")
