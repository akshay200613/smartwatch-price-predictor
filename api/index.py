from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Smartwatch Price Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

model = None

def get_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            try:
                model = joblib.load(MODEL_PATH)
            except Exception as e:
                print(f"Error loading model: {e}")
    return model

class SmartwatchFeatures(BaseModel):
    brand: str
    original_price: float
    rating: float
    num_ratings: int = 500

# Health check routes
@app.get("/health")
@app.get("/api/health")
def health_check():
    m = get_model()
    return {"status": "ok", "model_loaded": m is not None}

# Prediction routes (supports both /predict and /api/predict)
@app.post("/predict")
@app.post("/api/predict")
def predict_smartwatch(features: SmartwatchFeatures):
    m = get_model()
    if not m:
        raise HTTPException(status_code=503, detail="Model not loaded. Model file missing.")
    
    try:
        input_data = pd.DataFrame([{
            'Brand': features.brand,
            'Original Price': features.original_price,
            'Rating': features.rating,
            'Number OF Ratings': features.num_ratings
        }])
        
        prediction = m.predict(input_data)[0]
        return {"predicted_price": round(float(prediction), 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

# Frontend Static File Serving
@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, 'index.html')
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Smartwatch Price Predictor API is running"}

@app.get("/styles.css")
def serve_css():
    css_file = os.path.join(FRONTEND_DIR, 'styles.css')
    if os.path.exists(css_file):
        return FileResponse(css_file, media_type="text/css")
    raise HTTPException(status_code=404, detail="styles.css not found")

@app.get("/script.js")
def serve_js():
    js_file = os.path.join(FRONTEND_DIR, 'script.js')
    if os.path.exists(js_file):
        return FileResponse(js_file, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="script.js not found")
