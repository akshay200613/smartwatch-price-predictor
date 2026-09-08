from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Smartwatch Price Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = os.path.join(os.path.dirname(__file__), '../models/model.pkl')
try:
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        model = None
except Exception as e:
    print(f"Warning: Could not load model. {e}")
    model = None

class SmartwatchFeatures(BaseModel):
    brand: str
    original_price: float
    rating: float
    num_ratings: int

@app.post("/predict")
def predict_smartwatch(features: SmartwatchFeatures):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded. Run train_model.py first.")
    
    input_data = pd.DataFrame([{
        'Brand': features.brand,
        'Original Price': features.original_price,
        'Rating': features.rating,
        'Number OF Ratings': features.num_ratings
    }])
    
    prediction = model.predict(input_data)[0]
    return {"predicted_price": round(prediction, 2)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
