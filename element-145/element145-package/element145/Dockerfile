FROM python:3.12-slim

LABEL maintainer="Atlas Lattice Foundation <admin@atlaslattice.org>"
LABEL description="Element 145 — Sheldonbrain 144+1 Ontological Lattice API Server"
LABEL version="2.0.0"

WORKDIR /app

# Install dependencies
COPY pyproject.toml README.md ./
COPY element145/ ./element145/

RUN pip install --no-cache-dir ".[all]"

# Expose API port
EXPOSE 8145

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8145/health')" || exit 1

# Default: run REST API
ENTRYPOINT ["element145-api"]
CMD ["--host", "0.0.0.0", "--port", "8145"]
