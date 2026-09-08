from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Smartwatch Price Prediction API")

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve path to trained model file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')

model = None
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        print(f"Warning: Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"Warning: Could not load model. {e}")

class SmartwatchFeatures(BaseModel):
    brand: str
    original_price: float
    rating: float
    num_ratings: int = 500

@app.get("/api/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/api/predict")
def predict_smartwatch(features: SmartwatchFeatures):
    global model
    if not model:
        if os.path.exists(MODEL_PATH):
            try:
                model = joblib.load(MODEL_PATH)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
        
        if not model:
            raise HTTPException(status_code=503, detail="Model not loaded. Model file missing.")
    
    try:
        input_data = pd.DataFrame([{
            'Brand': features.brand,
            'Original Price': features.original_price,
            'Rating': features.rating,
            'Number OF Ratings': features.num_ratings
        }])
        
        prediction = model.predict(input_data)[0]
        return {"predicted_price": round(float(prediction), 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
