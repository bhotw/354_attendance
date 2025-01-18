# Base image for Raspberry Pi emulation
FROM balenalib/rpi-debian:bullseye

# Set working directory
WORKDIR /app

# Install Python and necessary tools
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy your application files into the container
COPY . /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Set the default command to run your application
CMD ["python3", "run.py"]

