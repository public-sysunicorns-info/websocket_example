FROM python:3.9 AS builder

# extra dependencies (over what buildpack-deps already includes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev

# Upgrade Pip
RUN python -m pip install --upgrade pip

# Create Python User on Container
RUN adduser --disabled-password python
USER python
WORKDIR /home/python
ENV PATH="/home/python/.local/bin:${PATH}"

# Prepare Dependencies
COPY --chown=python:python requirements.txt /home/python/wheels/requirements.txt
RUN pip wheel -r /home/python/wheels/requirements.txt -f /home/python/wheels

FROM python:3.9-slim

RUN python -m pip install --upgrade pip

# Create Python User on Container
RUN python -m pip install --upgrade pip
RUN adduser --disabled-password python
USER python
WORKDIR /home/python
ENV PATH="/home/python/.local/bin:${PATH}"

# Retrive previously build wheels
COPY --from=builder /home/python/wheels /home/python/wheels

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

COPY --chown=python:python requirements.txt .
RUN pip install --user -r requirements.txt -f /home/python/wheels

USER root
RUN rm -rf /home/python/wheels && rm -rf /home/python/.cache/pip/*

USER python
COPY --chown=python:python . .
CMD ["python", "./src/main.py"]