# Use an official Ultralytics image that includes YOLOv8 and PyTorch for CPU
FROM ultralytics/ultralytics:latest-cpu

# Set working directory
WORKDIR /app

# Paths are now relative to the project root build context (from docker-compose.yml)
# Install only your additional application-specific dependencies
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your model weights
COPY models /app/models

# Copy your FastAPI application code
COPY backend/app /app/app

# Expose the port FastAPI will run on
# This might already be exposed by the base image, but doesn't hurt to declare.
EXPOSE 8000

# Set the model path (if your app expects it here)
ENV MODEL_PATH=/app/models/last.pt

# Command to run your Uvicorn server for your FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 