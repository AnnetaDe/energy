# Use Python 3.11 (or your preferred version)
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project (including `main.py`)
COPY . .

# Expose FastAPI port
EXPOSE 8000

# ✅ Start FastAPI using absolute path
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

