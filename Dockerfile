# Dockerfile for Agents_Army
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY pyproject.toml setup.py ./
COPY src/ ./src/
COPY examples/ ./examples/

# Install package in editable mode
RUN pip install -e .

# Expose port for API (if implemented)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import agents_army; print('OK')" || exit 1

# Default command (can be overridden)
# Note: agents_army doesn't have a __main__.py, so we just run Python interactively
CMD ["python"]
