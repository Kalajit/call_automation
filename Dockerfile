FROM python:3.12-slim

# Install system dependencies including PortAudio and ffmpeg
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libportaudio2 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "call_chess_coach:app", "--host", "0.0.0.0", "--port", "$PORT"]