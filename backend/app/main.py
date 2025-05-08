from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os
from ultralytics import YOLO

# --- Configuration ---
MODEL_PATH = os.environ.get("MODEL_PATH", "/app/models/best.pt")

app = FastAPI(title="Human Detection API")
model = None  # Initialize model as None

@app.on_event("startup")
async def startup_event():
    global model
    try:
        model = YOLO(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"CRITICAL: Error loading model during startup: {e}")
        model = None
    
    if model is None:
        print(
            "WARNING: Model could not be loaded. "
            "API will not function correctly for detections."
        )
    else:
        print("FastAPI application started with model loaded.")

@app.post("/detect/")
async def detect_humans(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded or failed to load. Cannot perform detection."
        )

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload an image."
        )

    try:
        image_bytes = await file.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        results = model(pil_image, verbose=False)

        detections = []
        if results and results[0].boxes:
            for box in results[0].boxes:
                detections.append({
                    "box": box.xyxy[0].tolist(),
                    "confidence": float(box.conf[0]),
                    "class_id": int(box.cls[0]),
                    "class_name": model.names[int(box.cls[0])]
                })
        return JSONResponse(content={"detections": detections})
    except Exception as e:
        print(f"Error during detection: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error processing image: {str(e)}"
        )

@app.get("/")
async def root():
    return {
        "message": (
            "Human Detection API is running. Model status: "
            + ("Loaded" if model else "Not Loaded")
        )
    }