# Pinned Debian-based Python 3.11 base image
FROM python:3.11.8-slim-bookworm

# Install system dependencies (tar, gzip, bash, coreutils)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tar \
    gzip \
    bash \
    coreutils \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory for the agent
WORKDIR /workspace

# Copy application repository
COPY app/ /workspace/

# Install any python test dependencies (pytest for tests)
RUN pip install --no-cache-dir pytest==8.0.2

# Default command
CMD ["bash"]
