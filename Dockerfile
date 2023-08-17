FROM python:3.10.12-alpine3.18

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --user --no-cache-dir -r requirements.txt

COPY backend/ .

RUN python manage.py makemigrations && python manage.py migrate

CMD [ "python" ,"manage.py" ,"runserver" ,"0.0.0.0:8000" ]