from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import tempfile
import shutil

from utils.audio import preprocess_audio
from utils.classification import classify_meow
from utils.translation import translate_meow

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Meow2Text API",
    description="Translate your cat's meows to sassy text!",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Meow2Text API! 🐱"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Meow2Text is running! 😸"}

@app.post("/classify")
async def classify_audio(file: UploadFile = File(...)):
    """
    Classify uploaded cat meow audio into categories
    """
    try:
        # Validate file type
        if not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        # Preprocess audio
        processed_audio = preprocess_audio(temp_path)
        
        # Classify meow
        classification = classify_meow(processed_audio)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return JSONResponse(content=classification)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@app.post("/translate")
async def translate_audio(
    file: UploadFile = File(...),
    personality: str = "chill"
):
    """
    Translate cat meow to text with specified personality
    """
    try:
        # Validate file type
        if not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Validate personality
        valid_personalities = ["diva", "chill", "old_man"]
        if personality not in valid_personalities:
            raise HTTPException(status_code=400, detail=f"Personality must be one of: {valid_personalities}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        # Preprocess audio
        processed_audio = preprocess_audio(temp_path)
        
        # Classify meow
        classification = classify_meow(processed_audio)
        
        # Translate with personality
        translation = translate_meow(classification, personality)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return JSONResponse(content={
            "classification": classification,
            "translation": translation,
            "personality": personality
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.get("/personalities")
async def get_personalities():
    """
    Get available personality options
    """
    return {
        "personalities": [
            {
                "id": "diva",
                "name": "Diva",
                "description": "Dramatic and demanding cat",
                "emoji": "👑"
            },
            {
                "id": "chill",
                "name": "Chill",
                "description": "Laid-back and philosophical cat",
                "emoji": "😎"
            },
            {
                "id": "old_man",
                "name": "Old Man",
                "description": "Grumpy and wise cat",
                "emoji": "👴"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 