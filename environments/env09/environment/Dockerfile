# Pinned Debian-based Python 3.11 base image
FROM python:3.11.8-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    coreutils \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY app/ /workspace/

RUN pip install --no-cache-dir pytest==8.0.2

RUN python3 init_db.py

CMD ["bash"]
