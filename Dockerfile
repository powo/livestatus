FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
ENV PORT 8080
USER nobody
EXPOSE 8080

COPY ./app /app
