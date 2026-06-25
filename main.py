from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import pandas as pd


from analytics_engine import run_analysis

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Expense Budget Analyzer API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    else:
        return {"error": "Only CSV and Excel files are allowed"}

    
    required_columns = ["date_time", "category", "amount"]

    for col in required_columns:
        if col not in df.columns:
            return {"error": f"Missing required column: {col}"}

    if df.empty:
        return {"error": "Uploaded file is empty"}

    
    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(subset=["date_time", "amount"])

    if df.empty:
        return {"error": "No valid data after cleaning"}

   
    analysis_result = run_analysis(df)


    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "analysis": analysis_result
    }