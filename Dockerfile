FROM python:3.10.4 as base


FROM base as builder

ENV PYTHONUNBUFFERED 1

WORKDIR /home/app

EXPOSE 8000/tcp

RUN pip install --upgrade pip &&  \
    groupadd -r app_group &&  \
    useradd -d /home/app -r -g app_group app_user

COPY ./requirements /requirements
RUN pip install -r /requirements/base.txt --no-cache-dir

COPY --chown=app_user:app_group ./src .

USER app_user


FROM base as tests

WORKDIR /home/app

RUN pip install --upgrade pip &&  \
    groupadd -r app_group &&  \
    useradd -d /home/app -r -g app_group app_user
#COPY tests/functional/requirements.txt ./requirements_tests.txt

#COPY --from=builder --chown=app_user:app_group ./home/app .
#RUN #ls
RUN pip install -r /requirements/tests.txt --no-cache-dir

USER app_user

CMD ["gunicorn", "main:app", "-w", "10", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
