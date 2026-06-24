# Stage 1: Build dependencies
FROM python:3.11-slim as builder

# Set python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv directly from their official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml ./

COPY uv.lock ./

# Install dependencies using uv into the virtual environment
# (using --no-cache avoids saving downloaded packages to keep image small)
RUN uv pip install --no-cache -r pyproject.toml

# ==============================================================================
# Stage 2: Final runtime image
FROM python:3.11-slim

# Set python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
COPY . .

# Security Best Practice: Run the app as a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port your FastAPI app runs on
EXPOSE 8000

# Start the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
