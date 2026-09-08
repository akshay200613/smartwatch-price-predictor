import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer

# Page Config
st.set_page_config(page_title="Smartwatch Price Predictor", page_icon="⌚", layout="centered")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stButton>button { background-color: #3b82f6; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #2563eb; border: 1px solid #2563eb; }
    h1, h2, h3 { color: #60a5fa; }
    .success-text { color: #4ade80; font-size: 2.5rem; font-weight: bold; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("⌚ Smartwatch Price Predictor")
st.markdown("Estimate the market value of smartwatches based on specifications and brand power.")

# Paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'model.pkl')
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'smartwatches.csv')

@st.cache_resource
def load_or_train_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except:
            pass
            
    # Train if not exists
    st.info("Training model for the first time... Please wait.")
    df = pd.read_csv(DATA_PATH)
    for col in ['Current Price', 'Original Price', 'Rating', 'Number OF Ratings']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['Current Price', 'Original Price'])
    
    X = df[['Brand', 'Original Price', 'Rating', 'Number OF Ratings']]
    y = df['Current Price']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), ['Original Price', 'Rating', 'Number OF Ratings']),
            ('cat', Pipeline([('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), ['Brand'])
        ])
        
    model = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])
    model.fit(X, y)
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    st.success("Model trained successfully!")
    return model

model = load_or_train_model()

# UI Inputs
col1, col2 = st.columns(2)
with col1:
    brand = st.selectbox("Brand", ["noise", "boat", "fire-boltt", "apple", "samsung", "garmin"])
    rating = st.slider("Rating (1-5)", min_value=1.0, max_value=5.0, value=4.2, step=0.1)
with col2:
    original_price = st.number_input("Original Price (₹)", min_value=100, max_value=200000, value=5999)
    num_ratings = st.number_input("Number of Ratings", min_value=0, value=500)

if st.button("Predict Price"):
    input_data = pd.DataFrame([{
        'Brand': brand,
        'Original Price': original_price,
        'Rating': rating,
        'Number OF Ratings': num_ratings
    }])
    
    prediction = model.predict(input_data)[0]
    
    st.markdown("### Estimated Market Value:")
    st.markdown(f"<div class='success-text'>₹ {round(prediction):,}</div>", unsafe_allow_html=True)
    
st.markdown("---")
st.markdown("*Built with Streamlit • Random Forest Regressor Model*")
