# Use an official lightweight Python image.
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching.
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code.
COPY backend/ /app/

# Copy entrypoint.sh to the container root.
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the backend port (5000)
EXPOSE 5000

# Set the entrypoint script and command (for example, starting uvicorn)
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]