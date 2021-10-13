FROM python:3.9.6 AS builder

WORKDIR /wheels

# extra dependencies (over what buildpack-deps already includes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev
COPY requirements.txt /wheels/
RUN pip wheel -r requirements.txt -f /wheels

FROM python:3.9.6-slim

WORKDIR /opt/app

COPY --from=builder /wheels /wheels

ARG version
ARG version_long
ENV VERSION=$version
ENV VERSION_LONG=$version_long
ENV APPLICATION_VERSION=$version
ENV PATH "/opt/app/src:/root/.local:${PATH}"
ENV PYTHONPATH "/opt/app/src:/root/.local:{$PYTHONPATH}"
ENV LANG C.UTF-8

LABEL org.opencontainers.image.source=https://github.com/public-sysunicorns-info/websocket_example

EXPOSE 8080

COPY requirements.txt .
RUN pip install -r requirements.txt -f /wheels && rm -rf /wheels && rm -rf /root/.cache/pip/*

COPY . .

CMD ["python", "./src/main.py"]