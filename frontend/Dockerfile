FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV API_URL=http://backend:8000/logs

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
