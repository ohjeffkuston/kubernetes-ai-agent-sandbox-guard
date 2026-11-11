FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
COPY policy ./policy
RUN pip install --no-cache-dir . && useradd --uid 10001 --create-home guard
USER 10001
ENTRYPOINT ["agent-sandbox-guard"]

