FROM python:3.10-slim
RUN apt-get update && apt-get install -y ffmpeg gcc python3-dev
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir discord.py Flask requests yt-dlp pynacl imageio-ffmpeg
CMD ["python", "main.py"]
