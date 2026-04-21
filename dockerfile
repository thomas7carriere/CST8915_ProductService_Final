FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Flask service port
EXPOSE 3030

# Run with Gunicorn (production server)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:3030", "app:app"]