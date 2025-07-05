FROM python:3.12.10-alpine

RUN apk add --no-cache sqlite sqlite-dev gcc musl-dev libffi-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN uv pip install --system --no-cache --upgrade -r requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
