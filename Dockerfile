# Use an official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose the port Cloud Run uses
EXPOSE 8080

# Run FastAPI using Uvicorn (Change main:app if your file is named differently)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]