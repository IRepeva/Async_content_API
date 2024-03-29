FROM python:3.10.4 as base

ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 8000/tcp

RUN pip install --upgrade pip &&  \
    groupadd -r app_group &&  \
    useradd -d /app -r -g app_group app_user

COPY --chown=app_user:app_group ./requirements requirements
RUN pip install -r requirements/base.txt --no-cache-dir

COPY --chown=app_user:app_group ./app .

CMD ["gunicorn", "main:app", "-w", "10", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]


FROM base AS tests

WORKDIR /app

COPY --from=base --chown=app_user:app_group /app ./api

RUN pip install -r requirements/tests.txt --no-cache-dir

COPY --chown=app_user:app_group tests/functional .

USER app_user
