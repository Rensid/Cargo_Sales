FROM python:3.10

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /code/
ADD .env.docker /code/.env

CMD bash -c 'while !</dev/tcp/cargo_db/5432; do sleep 5; done; alembic upgrade head; python main.py'