FROM python:3.10.4 AS base

ENV PYTHONUNBUFFERED 1
ENV PATH /home/user/.local/bin:$PATH

RUN useradd -m user

WORKDIR /app

EXPOSE 8000/tcp

COPY ./requirements requirements
RUN pip install --user --upgrade pip && \
    pip install --user -r requirements/base.txt --no-cache-dir

COPY --chown=user app .
COPY --chown=user Makefile .
COPY --chown=user deploy/entrypoint.sh .

ENTRYPOINT ["/app/entrypoint.sh"]


FROM base AS prod

USER user

WORKDIR /app

COPY --chown=user --from=base /home .
COPY --chown=user --from=base /app .

CMD ["gunicorn", "main:app", "-w", "10", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]


FROM prod AS tests

USER root

WORKDIR /app

COPY --chown=user --from=prod /home .

RUN pip install --user -r requirements/tests.txt --no-cache-dir && \
    pip install --user -r requirements/base.txt --no-cache-dir

COPY --chown=user tests/functional .
