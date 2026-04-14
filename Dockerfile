# =============================================================================
# Dockerfile
# =============================================================================
# Builds a lightweight image with Gesta installed and a demo script ready
# to run. Uses a multi-stage build to keep the final image small.
#
# Build:
#   docker build -t gesta .
#
# Run demo:
#   docker run --rm gesta
#
# Run tests:
#   docker run --rm gesta pytest tests/ -v
#
# Interactive shell:
#   docker run --rm -it gesta bash
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1 — builder
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .
COPY README.md .

RUN uv sync --no-dev

# ---------------------------------------------------------------------------
# Stage 2 — runtime
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source
COPY gesta/ ./gesta/
COPY tests/  ./tests/
COPY scripts/ ./scripts/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

CMD ["python", "scripts/demo.py"]