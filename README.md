# Lupus Detector

AI-powered web app that classifies dermoscopic skin images as **LUPUS** or **Non-LUPUS** using a custom-trained YOLOv11 classification model, served through a FastAPI backend and a React + Three.js frontend.

![Python](https://img.shields.io/badge/Python-3.10-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green) ![React](https://img.shields.io/badge/React-19-blue) ![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-red)

## What it does

Upload a dermoscopic skin image → the model classifies it as LUPUS or Non-LUPUS in under 2 seconds, returning a confidence score and a full class-by-class breakdown.

> ⚠️ **Disclaimer:** This project is for educational and screening purposes only. It is not a medical device and is not a substitute for diagnosis by a qualified dermatologist or rheumatologist.

## How the model was trained

The classifier (`backend/best.pt`) was trained in [`Copy_of_LUPUS_Yolov11CustomObjectClassification.ipynb`](./Copy_of_LUPUS_Yolov11CustomObjectClassification.ipynb) on Google Colab (GPU runtime). The pipeline:

1. **Data prep** – LUPUS and Non-LUPUS images (shipped as `.rar` archives) are extracted and split 80/20 into `train/` and `val/` folders per class using a helper script (`extract_and_split_dataset`), with a fixed random seed for reproducibility.
2. **Training** – A YOLOv11 classification model (`yolo11s-cls.pt`, Ultralytics) is fine-tuned on the two-class dataset for 100 epochs at 640px image size:
   ```python
   from ultralytics import YOLO

   model = YOLO('yolo11s-cls.pt')
   results = model.train(data='/content/dataset_directory', epochs=100, imgsz=640)
   ```
3. **Validation** – The trained weights are validated with `model.val()`, reporting top-1/top-5 accuracy, plus a confusion matrix and training curves.
4. **Inference check** – The best checkpoint (`weights/best.pt`) is loaded and run against sample images to confirm predicted class and confidence before it's shipped to the backend.

To retrain or fine-tune the model yourself, open the notebook in Colab, supply your own `Lupus.rar` / `Non-lupus.rar` datasets, and run it top to bottom on a GPU runtime.

## Features

- YOLOv11 classifier trained on dermoscopic skin images
- FastAPI backend with a single `/predict` endpoint
- React frontend with an interactive Three.js 3D hero section
- Parallax editorial UI with Framer Motion animations
- Simple sign in / create account flow
- Animated per-class confidence breakdown
- Mobile responsive layout

## Project structure

```
lupus-detector/
├── Copy_of_LUPUS_Yolov11CustomObjectClassification.ipynb  # training notebook
├── backend/
│   ├── main.py            # FastAPI app (/predict endpoint)
│   ├── best.pt             # trained YOLOv11 classification weights
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── src/App.js           # UI, auth flow, Three.js hero, results view
    └── ...                  # standard Create React App scaffolding
```

## Tech Stack

| Layer      | Technology                      |
|------------|----------------------------------|
| ML Model   | YOLOv11 classification (Ultralytics) |
| Backend    | Python, FastAPI                 |
| Frontend   | React, Three.js, Framer Motion  |
| Deployment | Docker / Render                 |

## Local Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The backend loads `best.pt` from the `backend/` directory on the first prediction request.

### Frontend

```bash
cd frontend
npm install
npm start
```

By default the frontend expects the API at `http://localhost:8000`; update the fetch URL in `src/App.js` if you're pointing at a deployed backend instead.

### Docker (backend)

```bash
cd backend
docker build -t lupus-detector-backend .
docker run -p 7860:7860 lupus-detector-backend
```

## API

| Method | Endpoint  | Description                  |
|--------|-----------|-------------------------------|
| GET    | `/`       | Health check                  |
| POST   | `/predict`| Upload an image, get a prediction |

`/predict` expects a `multipart/form-data` request with an image file under the `file` field, and rejects non-image content types.

### Response example

```json
{
  "label": "LUPUS",
  "confidence": 96.8,
  "is_lupus": true,
  "breakdown": [
    { "name": "LUPUS", "probability": 96.8 },
    { "name": "Non-LUPUS", "probability": 3.2 }
  ],
  "image_size": "294 × 222",
  "analyzed_at": "2026-07-09 12:00",
  "model": "YOLOv11 classifier"
}
```

## Disclaimer

For educational and screening purposes only. Not a substitute for professional medical diagnosis.
