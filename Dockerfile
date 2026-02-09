FROM python:3.12-slim

RUN echo "deb http://deb.debian.org/debian bookworm contrib non-free" > /etc/apt/sources.list.d/contrib.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        libreoffice-writer \
        fonts-liberation \
        fonts-dejavu \
        fonts-freefont-ttf \
        fonts-noto \
        ttf-mscorefonts-installer \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/

RUN mkdir -p /app/output && chown -R 1000:1000 /app

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app/src

ENTRYPOINT ["/app/entrypoint.sh"]