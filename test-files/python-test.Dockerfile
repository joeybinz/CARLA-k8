
FROM python:3.7

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir carla==0.9.14

COPY python-test.py .

CMD [ "python", "./python-test.py" ]
