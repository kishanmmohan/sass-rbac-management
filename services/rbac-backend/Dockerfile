FROM python:3.13-slim

WORKDIR /usr/src/api

RUN apt-get update && apt-get install -y \
  python3-dev \
  gcc \
  g++ \
  make \
  pkg-config \
  libffi-dev \
  libc-dev \
  libgl1-mesa-glx \
  libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel build

COPY requirements.txt .

# Install requirements
RUN pip install --no-build-isolation --prefer-binary -r requirements.txt

# Copy the rest of the application
COPY src/ .

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
