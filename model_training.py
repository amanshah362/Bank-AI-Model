import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# Load your data
bank = pd.read_csv(r"C:\\Users\\iaman\\ML\\MACHINE LEARNING PROJECTS\\Datasets\\bank-full.csv", sep=';')

# Prepare features
oe_features = ['default', 'housing', 'loan', 'education', 'poutcome']
ohe_features = ['job', 'marital', 'contact', 'month']
num_features = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']

X = bank.drop(columns='y')
y = bank['y'].apply(lambda x: 1 if x == 'yes' else 0)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.25, random_state=41
)

# Create pipeline
preprocessor = ColumnTransformer([
    ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ohe_features),
    ('oe', OrdinalEncoder(), oe_features),
    ('num', RobustScaler(), num_features)
])

LR = LogisticRegression(class_weight='balanced', max_iter=5000)
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LR)
])

# Train model
model.fit(X_train, y_train)

# Save the model
with open('models/bank.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model saved successfully!")
print(f"Train Accuracy: {model.score(X_train, y_train):.3f}")
print(f"Test Accuracy: {model.score(X_test, y_test):.3f}")