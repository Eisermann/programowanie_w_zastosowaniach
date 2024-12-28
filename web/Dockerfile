FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpango-1.0-0 libpangoft2-1.0-0

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
