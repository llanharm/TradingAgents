FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build
COPY . .
RUN pip install --no-cache-dir .

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create a dedicated user and ensure the data directory exists for
# storing API keys and cached results between container runs.
# Mount a volume at /home/appuser/.tradingagents to persist data.
RUN useradd --create-home appuser \
 && install -d -m 0755 -o appuser -g appuser /home/appuser/.tradingagents
USER appuser
WORKDIR /home/appuser/app

COPY --from=builder --chown=appuser:appuser /build .

# Expose a TRADINGAGENTS_DATA_DIR env var so the app can find the
# persistent data directory without hardcoding the path in configs.
ENV TRADINGAGENTS_DATA_DIR=/home/appuser/.tradingagents

# Set a default log level that's useful for personal/dev use without
# being too noisy. Override with -e TRADINGAGENTS_LOG_LEVEL=DEBUG if needed.
ENV TRADINGAGENTS_LOG_LEVEL=WARNING

# Default to showing help if no subcommand is provided, which is friendlier
# than the default error message when running the container without arguments.
ENTRYPOINT ["tradingagents"]
CMD ["--help"]
