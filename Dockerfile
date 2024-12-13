# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
ENV PORT 8080
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./

RUN mkdir state_db
RUN uv sync

EXPOSE ${PORT}

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "web_server.py"]