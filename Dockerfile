FROM python:2.7.17-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w 1", "-b 0.0.0.0:5000", "app:app"]
