FROM python:3.9-slim
WORKDIR /app

# Paths are relative to the build context set in docker-compose.yml (which is ./frontend)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501
ENV FASTAPI_URL=http://localhost:8000/detect/
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 