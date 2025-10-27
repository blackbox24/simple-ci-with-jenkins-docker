FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies and clean up
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip install --no-cache-dir wheel && \
    pip wheel --no-cache-dir  --wheel-dir /app/tmp/wheels -r requirements.txt

FROM python:3.12-slim

# Create non-root user and group
RUN groupadd -r appuser && \
    useradd -r -g appuser -m -d /home/appuser appuser

WORKDIR /app

COPY --from=builder /app/tmp/wheels /app/tmp/wheels

RUN pip install --no-cache-dir /app/tmp/wheels/* && \
    rm -rf /app/tmp/wheels

COPY --chmod=appuser:appuser . .

# Switch to non-root user
USER appuser

# RUN CUSTOM COMMANDS
EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
