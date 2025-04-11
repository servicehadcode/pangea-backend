FROM python:3.9-slim

# First install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    portaudio19-dev \
    libasound2-dev \
    libffi-dev \
    python3-dev \
    portaudio19-dev \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip first
RUN pip install --upgrade pip

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the rest of the app
COPY . .

ENV PATH = /root/.local/bin:$PATH
ENV FLASK_APP = src/app.py
ENV PORT = 5000
ENV MONGODB_URI=mongodb://mongo:27017
ENV MONGODB_DB=pangea


EXPOSE 5000
CMD ["python3", "src/app.py"]