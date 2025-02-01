FROM python:3.10-slim
WORKDIR /app
COPY backend /app/backend
COPY frontend /app/frontend
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "backend/app.py"]
