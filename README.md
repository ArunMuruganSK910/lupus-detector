\# Lupus Detector



AI-powered lupus skin disease detection using YOLOv8 deep learning model.



!\[Python](https://img.shields.io/badge/Python-3.10-blue) !\[FastAPI](https://img.shields.io/badge/FastAPI-0.136-green) !\[React](https://img.shields.io/badge/React-18-blue) !\[YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red)



\## What it does



Upload a dermoscopic skin image → YOLOv8 classifies it as Lupus or Non-Lupus in under 2 seconds, with confidence scores and a full breakdown.



\## Features



\- YOLOv8 classifier trained on dermoscopic skin images

\- FastAPI backend with `/predict` endpoint

\- React frontend with Three.js 3D interactive hero

\- Parallax editorial UI with Framer Motion animations

\- Auth system (sign in / create account)

\- Confidence breakdown with animated bars

\- Mobile responsive



\## Tech Stack



| Layer | Technology |

|-------|-----------|

| ML Model | YOLOv8 (Ultralytics) |

| Backend | Python, FastAPI |

| Frontend | React, Three.js, Framer Motion |

| Deployment | Render |



\## Local Setup



\### Backend

```bash

cd backend

python -m venv venv

venv\\Scripts\\activate

pip install fastapi uvicorn python-multipart ultralytics pillow numpy

uvicorn main:app --reload --port 8000

```



\### Frontend

```bash

cd frontend

npm install

npm start

```



\## API



| Method | Endpoint | Description |

|--------|----------|-------------|

| GET | `/` | Health check |

| POST | `/predict` | Upload image, get prediction |



\### Response example

```json

{

&#x20; "label": "LUPUS",

&#x20; "confidence": 96.8,

&#x20; "is\_lupus": true,

&#x20; "breakdown": \[

&#x20;   {"name": "LUPUS", "probability": 96.8},

&#x20;   {"name": "Non-LUPUS", "probability": 3.2}

&#x20; ],

&#x20; "image\_size": "294 × 222",

&#x20; "analyzed\_at": "2026-06-01 12:00",

&#x20; "model": "YOLOv8 classifier"

}

```



\## Disclaimer



For educational and screening purposes only. Not a substitute for professional medical diagnosis.

