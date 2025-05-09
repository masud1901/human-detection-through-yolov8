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

## Building and Pushing Docker Images

A utility script `build_and_push.sh` is provided in the project root to simplify the process of building the Docker images for both the backend and frontend services and pushing them to Docker Hub.

### Script Overview

The script performs the following actions:

1.  Builds the backend Docker image using `backend/Dockerfile` and tags it.
2.  Builds the frontend Docker image using `frontend/Dockerfile` and tags it.
3.  Pushes both tagged images to Docker Hub.

### Configuration

Before running the script, you might want to review or modify the following variables at the top of `build_and_push.sh`:

-   `DOCKER_HUB_USERNAME`: Set this to your Docker Hub username. (Default: "ayon1901")
-   `BACKEND_IMAGE_NAME`: Name for the backend image. (Default: "human-detection-backend")
-   `FRONTEND_IMAGE_NAME`: Name for the frontend image. (Default: "human-detection-frontend")
-   `TAG`: The tag for the images. (Default: "latest")

### Prerequisites

-   Ensure Docker is running.
-   You must be logged into Docker Hub via the command line. If not, run:
    ```bash
    docker login
    ```
    and enter your Docker Hub credentials.

### Usage

To run the script, navigate to the project root directory in your terminal and execute:

```bash
bash build_and_push.sh
```

This will build the images and push them to the configured Docker Hub repository.

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

## Deployment to AWS EC2 (Alternative)

While the project is designed for Railway, it was also successfully deployed to an AWS EC2 instance (free-tier Amazon Linux). This section details key steps and learnings from that process, which can be adapted for similar cloud VM deployments.

### Key Steps & Learnings:

1.  **EC2 Instance Setup:**
    -   Launched a free-tier Amazon Linux EC2 instance.
    -   SSH access is required for setup.

2.  **Disk Space Management (Crucial):**
    -   The default 8GB root volume on free-tier instances can be insufficient for Docker images, especially those with ML libraries.
    -   **Symptom:** `docker-compose up --build` or `docker pull` failing with "no space left on device".
    -   **Solution:**
        -   Attached a new EBS volume (e.g., 20GB) to the EC2 instance.
        -   Formatted the new volume (e.g., `sudo mkfs -t ext4 /dev/xvdf` - *Note: device name like `/dev/xvdf` or `/dev/nvme1n1` may vary depending on the instance type and virtualization*).
        -   Stopped the Docker service (`sudo systemctl stop docker`).
        -   Created a mount point: `sudo mkdir -p /var/lib/docker` (or ensured the old one was empty if it existed on the root volume).
        -   Mounted the new volume to `/var/lib/docker`: `sudo mount /dev/xvdf /var/lib/docker`.
        -   **Made the mount permanent:** Added an entry to `/etc/fstab` using the volume's UUID (e.g., `UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx /var/lib/docker ext4 defaults,nofail 0 2`). This ensures Docker uses the larger volume for its images, containers, and build cache.
        -   Restarted Docker (`sudo systemctl start docker`).

3.  **Docker & Docker Compose Installation:**
    -   Installed Docker and Docker Compose on the EC2 instance following the official documentation for Amazon Linux.

4.  **Cloning the Repository & Model:**
    -   Cloned the project repository onto the EC2 instance.
    -   Ensured the model file (`models/last.pt`) was in place.

5.  **Building and Running:**
    -   Used `docker-compose up --build -d` to build and run the application.

6.  **Security Group Configuration:**
    -   **Symptom:** Application running (verified with `docker ps` and logs) but not accessible via the EC2 public IP in a browser.
    -   **Solution:** Configured the EC2 instance's Security Group to allow inbound TCP traffic on the port used by the frontend (e.g., `8501`) from `0.0.0.0/0` (for public access during testing) or a specific IP for better security.

7.  **Application Stability:**
    -   Encountered an issue where containers were in a restart loop due to a missing dependency (`dill` for the backend) being installed at runtime and requiring a restart.
    -   **Solution:** Added the missing dependency to the backend's `requirements.txt` and rebuilt the Docker image, ensuring all dependencies are included in the image itself for stability.

This EC2 deployment process highlights common challenges in moving containerized applications to cloud VMs, particularly around storage, network configuration, and ensuring application dependencies are correctly packaged.

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
