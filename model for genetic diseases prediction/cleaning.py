import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the raw training dataset
df = pd.read_csv("./train.csv")

# Drop irrelevant columns
columns_to_drop = [
    'Patient Id', 'Patient First Name', 'Family Name', 'Father\'s name',
    'Institute Name', 'Location of Institute', 'Disorder Subclass'
]
df = df.drop(columns=columns_to_drop)

# Drop rows with missing target values
df = df.dropna(subset=['Genetic Disorder'])

# Fill missing numerical values with median
num_cols = df.select_dtypes(include=['float64', 'int']).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# Fill missing categorical values with mode
cat_cols = df.select_dtypes(include=['object']).columns.drop('Genetic Disorder')
df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])

# Encode categorical variables
label_encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Encode target column
target_le = LabelEncoder()
df['Genetic Disorder'] = target_le.fit_transform(df['Genetic Disorder'])

# Final cleaned DataFrame ready for training
print("Cleaned dataset shape:", df.shape)
print(df.head())
