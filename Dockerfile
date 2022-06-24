FROM python:3.10.4

ENV PYTHONUNBUFFERED 1

WORKDIR /home/app

EXPOSE 8000/tcp

RUN pip install --upgrade pip &&  \
    groupadd -r app_group &&  \
    useradd -d /home/app -r -g app_group app_user

COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY --chown=app_user:app_group ./src .

#USER app_user

CMD ["gunicorn", "main:app", "-w", "10", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
