import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the dataset
df = pd.read_csv('diabetes_data_upload.csv')

print("First look at data:")
print(df.head())

# Convert Yes/No and Positive/Negative to numbers
le = LabelEncoder()
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = le.fit_transform(df[col])

print("\nAfter encoding:")
print(df.head())

# Split into features and target
X = df.drop('class', axis=1)
y = df['class']

print("\nFeatures:", X.columns.tolist())

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)

# Build and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
print("\nTraining the model...")
model.fit(X_train, y_train)
print("Training done!")

# Test the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

print("\nDetailed Report:")
print(classification_report(y_test, y_pred))

# Show which symptoms matter most
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nMost important symptoms for prediction:")
print(feature_importance)

# Save the model
joblib.dump(model, 'diabetes_model_v2.pkl')
print("\nModel saved as diabetes_model_v2.pkl!")