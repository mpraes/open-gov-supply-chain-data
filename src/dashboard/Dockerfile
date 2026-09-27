FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY src ./src
RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=src
ENV DASHBOARD_ENV_FILE=/app/.env
EXPOSE 8050
CMD ["uvicorn", "dashboard.app:app", "--host", "0.0.0.0", "--port", "8050"]
