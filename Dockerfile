FROM python:3.10-slim

# Add build tools + OpenGL + NumPy headers
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    libgl1-mesa-glx \
    libglu1-mesa \
    libx11-6 \
    libxext6 \
    libxi6 \
    python3-opengl \
    python3-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install pip packages (numpy first for headers)
RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "Ray-Gui.py", "--server.port=10000", "--server.address=0.0.0.0"]
