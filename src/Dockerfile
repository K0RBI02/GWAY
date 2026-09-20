FROM python:3.12-alpine

# Build-Tools nur für den Fall, dass eine Abhängigkeit kein fertiges ARM-Wheel hat
RUN apk add --no-cache --virtual .build gcc musl-dev libffi-dev \
 && pip install --no-cache-dir tplinkrouterc6u \
 && apk del .build

WORKDIR /app
COPY server.py /app/server.py
COPY static /app/static

CMD ["python3", "/app/server.py"]
