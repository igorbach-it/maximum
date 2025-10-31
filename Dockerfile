FROM alpine:3.20

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache \
      python3 py3-pip bash curl ca-certificates \
      supervisor ttyd

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN adduser -D -s /bin/bash dev
WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Код и конфиги
COPY app.py ./
COPY cli/ ./cli/
COPY libs/ ./libs/
COPY supervisord.conf start.sh ./

RUN chown -R dev:dev /app && chmod +x /app/start.sh
USER dev

EXPOSE 8000 7681

# healthcheck только к API
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD curl -fsS http://127.0.0.1:8000/healthz || exit 1

# корректные сигналы для supervisor
STOPSIGNAL SIGTERM

CMD ["./start.sh"]
