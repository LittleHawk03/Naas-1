
FROM python:3.10.12-alpine3.18 as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt


FROM python:3.10.12-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY backend/ .

# Lenh duoi dung khi ma su dung database sqllite3

# RUN python manage.py makemigrations && python manage.py migrate

# CMD [ "python" ,"manage.py" ,"runserver" ,"0.0.0.0:8000" ]




