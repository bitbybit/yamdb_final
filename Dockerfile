FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY api_yamdb/ /app

WORKDIR /app

RUN python3 manage.py migrate
RUN python manage.py import_csv

CMD ["python3", "manage.py", "runserver", "0:8000"]
