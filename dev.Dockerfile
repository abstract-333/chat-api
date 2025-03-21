FROM ghcr.io/astral-sh/uv:0.6.7-python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --group test

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --group test

# It is important to use the image that matches the builder, as the path to the
# Python executable must be the same, e.g., using `python:3.12-slim-bookworm`
# will fail.
FROM python:3.13-slim-bookworm

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app


WORKDIR /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "--factory", "application.api.main:create_app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
