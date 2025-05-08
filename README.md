# Human Detection Application

This project is a web application that detects humans in uploaded images. It uses a YOLO (You Only Look Once) object detection model served via a FastAPI backend, with a user-friendly Streamlit frontend.

## Features

-   **Human Detection:** Identifies humans in images using a YOLO model (`last.pt`).
-   **Web Interface:** Allows users to upload images through a Streamlit application.
-   **Adjustable Confidence:** Users can set a confidence threshold to filter detections.
-   **Dual Image View:** Displays both the original and processed image with bounding boxes.
-   **API Backend:** Object detection logic is handled by a robust FastAPI backend.
-   **Dockerized:** Fully containerized with Docker and Docker Compose for easy local setup and deployment.
-   **Deployable:** Designed for easy deployment on platforms like Railway.

## Tech Stack

-   **Backend:** FastAPI, Uvicorn, Python
-   **Frontend:** Streamlit, Python, Requests
-   **Object Detection:** YOLO (via Ultralytics library), `last.pt` model weights
-   **Containerization:** Docker, Docker Compose
-   **Deployment Target:** Railway (or any platform supporting Docker containers)

## Project Structure

```
human_detection/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py         # FastAPI logic, model loading, inference
│   ├── Dockerfile          # Dockerfile for the backend
│   └── requirements.txt    # Python dependencies for backend
├── frontend/                 # Streamlit application
│   ├── app.py              # Streamlit UI and logic
│   ├── Dockerfile          # Dockerfile for the frontend
│   └── requirements.txt    # Python dependencies for frontend
├── models/                   # Trained model weights
│   └── last.pt             # Currently used model (best.pt had loading issues)
│   └── best.pt             # (Placeholder or original best model)
├── .gitignore                # Specifies intentionally untracked files
└── docker-compose.yml      # For local multi-container Docker setup
└── README.md                 # This file
```

## Local Setup & Running

### Prerequisites

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)
-   Git

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repo-name>
    ```

2.  **Place Model File:**
    Ensure your trained model file (currently configured to use `last.pt`) is in the `models/` directory.
    ```bash
    models/last.pt
    ```

3.  **Build and Run with Docker Compose:**
    This command will build the Docker images for the backend and frontend services and then start them.
    ```bash
    docker-compose up --build
    ```
    To run in detached mode (in the background):
    ```bash
    docker-compose up --build -d
    ```

4.  **Access the Application:**
    -   **Streamlit Frontend:** Open your web browser and go to `http://localhost:8501`
    -   **FastAPI Backend (Docs):** You can access the API documentation at `http://localhost:8000/docs`

5.  **Stopping the Application:**
    -   If running in the foreground, press `Ctrl+C` in the terminal where `docker-compose up` is running.
    -   If running in detached mode, use: `docker-compose down`

### Environment Variables (for local testing without Docker Compose for frontend)

-   The frontend (`frontend/app.py`) expects the `FASTAPI_URL` environment variable to point to the backend's detection endpoint. `docker-compose.yml` sets this automatically for container-to-container communication.
-   The backend (`backend/app/main.py`) uses `MODEL_PATH` (defaulted in its Dockerfile) to locate the model file within its container.

## Model Used

The application currently uses `last.pt` due to issues encountered with loading `best.pt` (related to potential file corruption or version incompatibility). The `MODEL_PATH` environment variable in `backend/Dockerfile` is set accordingly.

## Deployment to Railway

This application is structured for easy deployment to [Railway](https://railway.app/).

1.  Push your project to a GitHub repository.
2.  On Railway, create a new project and deploy from your GitHub repo.
3.  **Backend Service:**
    -   Set the service's root directory to `./backend`.
    -   Railway will use `backend/Dockerfile`.
    -   Ensure port 8000 is exposed.
4.  **Frontend Service:**
    -   Set the service's root directory to `./frontend`.
    -   Railway will use `frontend/Dockerfile`.
    -   Ensure port 8501 is exposed.
    -   **Crucially, set the environment variable `FASTAPI_URL`** for the frontend service to `http://<your-railway-backend-service-name>:8000/detect/`. Replace `<your-railway-backend-service-name>` with the actual name Railway gives your backend service.

## API Endpoint

-   **`POST /detect/`**
    -   Accepts an image file upload.
    -   Returns JSON with detection details (bounding boxes, confidence, class).
    -   Example response:
        ```json
        {
          "detections": [
            {
              "box": [x_min, y_min, x_max, y_max],
              "confidence": 0.83,
              "class_id": 0,
              "class_name": "Human"
            }
          ]
        }
        ```
