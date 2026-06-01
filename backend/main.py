from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ultralytics import YOLO
import numpy as np
import io
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

def load_model():
    global model
    if model is None:
        model = YOLO("best.pt")
    return model

@app.get("/")
def home():
    return {"message": "Lupus Detector API is running!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        m = load_model()
        results = m(image)
        r = results[0]

        if hasattr(r, "probs") and r.probs is not None:
            idx = r.probs.top1
            conf = float(r.probs.top1conf)
            probs = r.probs.data.cpu().numpy()
            names = list(m.names.values())

            breakdown = [
                {"name": names[i], "probability": round(float(probs[i]) * 100, 1)}
                for i in range(len(names))
            ]

            return {
                "label": names[idx],
                "confidence": round(conf * 100, 1),
                "is_lupus": names[idx].upper() == "LUPUS",
                "breakdown": breakdown,
                "image_size": f"{image.width} × {image.height}",
                "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "model": "YOLOv8 classifier"
            }

        raise HTTPException(status_code=500, detail="Model returned no results")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))