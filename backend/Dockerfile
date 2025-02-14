# Stage 1: Build the package
FROM python:3.13-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Set the timezone
ENV TZ=Europe/Helsinki
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Git and build dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools wheel build

# Copy source files
COPY pyproject.toml ./
COPY src ./src

# Build the package
RUN python -m build

# Stage 2: Install the built package only (no Git needed)
FROM python:3.13-slim

WORKDIR /app

# Install Git (needed for installing git packages)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy built package
COPY --from=builder /app/dist/*.whl ./

# Copy the source code into the container (for running scripts)
COPY src ./src
COPY creds ./creds
COPY app.py ./
COPY terminal.py ./

# Install the built package
RUN pip install --no-cache-dir *.whl

# Expose port 5000 for the Flask application
EXPOSE 5000

# Run the Flask application using waitress (Works in Windows and Linux)
CMD ["waitress-serve", "--listen=0.0.0.0:5000", "app:app"]