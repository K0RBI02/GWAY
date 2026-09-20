FROM python:3.12-alpine

# Build tools are only needed if a dependency has no prebuilt ARM wheel
COPY requirements.txt /tmp/requirements.txt
RUN apk add --no-cache --virtual .build gcc musl-dev libffi-dev \
 && pip install --no-cache-dir -r /tmp/requirements.txt \
 && apk del .build

WORKDIR /app
COPY server.py /app/server.py
COPY static /app/static

CMD ["python3", "/app/server.py"]
