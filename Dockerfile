version: '3.8'

services:
  postgres:
    image: postgres:latest
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-llmcoder}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
      POSTGRES_DB: ${POSTGRES_DB:-llmcoder_db}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:latest
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app/backend
      - ./projects:/app/projects
      - backend_data:/app/backend_data
    environment:
      - OLLAMA_HOST=http://host.docker.internal:11434
      - HF_TOKEN=${HF_TOKEN}
      - DATABASE_URL=postgresql://llmcoder:password@postgres:5432/llmcoder_db
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app/frontend
    environment:
      - VITE_API_BASE_URL=http://localhost:5000/api
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
  backend_data: