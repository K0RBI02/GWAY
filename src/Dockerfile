FROM python:3.12-alpine

# Build tools are only needed if a dependency has no prebuilt ARM wheel
COPY requirements.txt /tmp/requirements.txt
RUN apk add --no-cache --virtual .build gcc musl-dev libffi-dev \
 && pip install --no-cache-dir -r /tmp/requirements.txt \
 && apk del .build

WORKDIR /app
COPY server.py /app/server.py
COPY icon.png /app/icon.png
COPY static /app/static

# Health check: Home Assistant uses the container health status instead of the obsolete "watchdog" option
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8480/api/state', timeout=4)"

CMD ["python3", "/app/server.py"]
