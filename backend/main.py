from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from model import TenKAnalyzer
import tempfile

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tenkanalyzer.onrender.com",  # Your Vercel domain
        "http://localhost:3000"  # Keep local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

analyzer = TenKAnalyzer(api_key)

@app.post("/analyze")
async def analyze_10k(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Analyze the PDF
        analysis = analyzer.analyze_10k(tmp_path)
        return analysis
    finally:
        # Clean up temporary file
        os.unlink(tmp_path)