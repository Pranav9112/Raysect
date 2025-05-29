FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    python3-dev \
    pkg-config \
    libgl1-mesa-glx \
    libglu1-mesa \
    libx11-6 \
    libxext6 \
    libxi6 \
    python3-opengl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

# Install Cython before raysect to compile pyx files
RUN pip install numpy --no-cache-dir
RUN pip install cython --no-cache-dir

# Now raysect from source to force build
RUN pip uninstall -y raysect
RUN pip install --no-binary :all: raysect

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "Ray-Gui.py", "--server.port=10000", "--server.address=0.0.0.0"]
