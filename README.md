
# FastAPI Test

<https://fastapi.tiangolo.com/deployment/>

```bash
mkdir livestatus
cd livestatus/
vim Dockerfile
mkdir app
vim app/main.py
docker build -t livestatus .
docker run -d --rm --name livestatus -p 8000:80 livestatus
docker logs -f livestatus
```

