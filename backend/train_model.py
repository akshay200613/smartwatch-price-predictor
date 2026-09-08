import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
import joblib
import os

os.makedirs(os.path.join(os.path.dirname(__file__), '../models'), exist_ok=True)

print("Training Smartwatch Pricing Model...")
try:
    data_path = os.path.join(os.path.dirname(__file__), '../data/smartwatches.csv')
    df = pd.read_csv(data_path)
    df = df.dropna(subset=['Current Price', 'Original Price'])
    
    for col in ['Current Price', 'Original Price', 'Rating', 'Number OF Ratings']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    df = df.dropna(subset=['Current Price', 'Original Price'])

    X = df[['Brand', 'Original Price', 'Rating', 'Number OF Ratings']]
    y = df['Current Price']

    numeric_features = ['Original Price', 'Rating', 'Number OF Ratings']
    categorical_features = ['Brand']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), numeric_features),
            ('cat', Pipeline([('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), categorical_features)
        ])

    model = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

    model.fit(X, y)
    
    model_path = os.path.join(os.path.dirname(__file__), '../models/model.pkl')
    joblib.dump(model, model_path)
    print("Saved model to models/model.pkl")
except Exception as e:
    print(f"Error training model: {e}")
