FROM python:3.11-alpine

RUN pip install --upgrade pip --no-cache

WORKDIR /usr/src/app/

# Requirements

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

# Ports and run

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]