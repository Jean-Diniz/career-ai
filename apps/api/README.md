# README

Guia rápido para Docker + FastAPI/Uvicorn em modo dev com hot-reload e instalação dinâmica de pacotes.

---

## Build da imagem

```bash
docker build -t fastapi-image:dev .
```

## Execução com hot-reload

```bash
docker run --rm --name fastapi-container \
  -p 8000:80 \
  -v "$(pwd)":/code \
  fastapi-image:dev \
  uvicorn app.main:app --host 0.0.0.0 --port 80 --reload

```

Acesse: `http://localhost:8000`

---

## Instalar pacotes em runtime

```bash
docker exec -it fastapi-container uv pip install pyjwt --system --no-cache
docker restart fastapi-container
```

---

## Atualizar `requirements.txt`

```bash
docker exec fastapi-container uv pip freeze --system > requirements.txt
```

**Pronto!**
