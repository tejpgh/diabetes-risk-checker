import pandas as pd

# Load the dataset
df = pd.read_csv('diabetes_data_upload.csv')

print("Shape of dataset:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nUnique values in each column:")
for col in df.columns:
    print(f"{col}: {df[col].unique()}")

print("\nHow many Diabetic vs Non Diabetic:")
print(df['class'].value_counts())