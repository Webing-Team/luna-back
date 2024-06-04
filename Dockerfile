FROM python:3.11.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y python3.11-dev build-essential  # Install development headers

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY . /code/
CMD ["python", "/code/manage.py", "makemigrations"]
CMD ["python", "/code/manage.py", "migrate"]
CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]