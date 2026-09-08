# ⌚ Smartwatch Price Predictor

An Machine Learning application that estimates the market value of smartwatches based on brand, original price, ratings, and customer reviews using Random Forest Regression.

## 🚀 Live Demo

**Web Application**: [https://smartwatch-price-predictor-dal93r7z9-med-ai3.vercel.app/](https://smartwatch-price-predictor-dal93r7z9-med-ai3.vercel.app/)

---

## 📌 Features

- **Machine Learning Pricing Model**: Trained on smartwatch market dataset using Random Forest Regressor and Scikit-Learn pipelines.
- **FastAPI Serverless Backend**: High-performance RESTful API powering real-time price predictions.
- **Interactive Web Interface**: Responsive HTML5, CSS3, and JavaScript frontend with dark glassmorphism styling.
- **Streamlit App Option**: Also includes a standalone Streamlit dashboard (`app.py`) for quick exploratory analysis.

---

## 🛠️ Tech Stack

- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib
- **Backend API**: FastAPI, Uvicorn, Pydantic
- **Frontend**: HTML5, Vanilla CSS3, JavaScript (Fetch API)
- **Dashboard**: Streamlit
- **Deployment**: Vercel (Python Serverless Function)

---

## 💻 Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/akshay200613/smartwatch-price-predictor.git
cd smartwatch-price-predictor
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application

#### Option A: Streamlit Dashboard
```bash
streamlit run app.py
```

#### Option B: FastAPI Backend & Frontend
```bash
uvicorn api.index:app --reload --port 8000
```
Open `http://localhost:8000` in your browser.

---

## 📁 Project Structure

```
smartwatch_project/
│
├── api/
│   └── index.py            # Vercel FastAPI Serverless entrypoint
├── backend/
│   ├── main.py             # FastAPI local development app
│   └── train_model.py      # ML model training script
├── data/
│   └── smartwatches.csv    # Dataset
├── frontend/
│   ├── index.html          # Web UI HTML structure
│   ├── styles.css          # Modern dark mode styling
│   └── script.js            # Frontend API logic
├── models/
│   └── model.pkl           # Pre-trained Random Forest model
├── notebooks/              # Jupyter notebooks for EDA & model analysis
├── app.py                  # Streamlit application
├── vercel.json             # Vercel deployment routing configuration
└── requirements.txt        # Python package dependencies
```

---

## 📄 License
This project is open source and available under the MIT License.
