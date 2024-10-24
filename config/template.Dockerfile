# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

# Read aws creds
ENV AWS_ACCESS_KEY
ENV AWS_SECRET_KEY
ENV AWS_BUCKET

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install S3 dependencies
RUN apt-get update -y && \
  apt-get install -y \
    s3fs \
    libfuse-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libssl-dev \
    mime-support \
    automake \
    libtool \
    wget \
    tar \
    git \
    unzip &&
    apt-get clean

RUN pip --no-cache-dir install --upgrade awscli
RUN mkdir -p /mnt/s3


# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=algo/,target=algo/ \
    python -m pip install ./algo

# Switch to the non-privileged user to run the application.
USER appuser

VOLUME ["/output"]

# Define input / output files
ENV INPUT_FILE=""
ENV OUTPUT_FILE=""
# Run the application
# NOTE: edit the second command
CMD s3fs ${AWS_BUCKET} /mnt/s3; python3 -m algo "/mnt/s3/input/${INPUT_FILE}" "/output/${OUTPUT_FILE}"
