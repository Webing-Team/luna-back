FROM python:3.11.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY config/requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code/