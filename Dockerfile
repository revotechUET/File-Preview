FROM python:2.7.17-alpine

WORKDIR /app

ENV BUDGET_URL=https://users.i2g.cloud
ENV SERVICE=WI_PROJECT_STORAGE

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-b 0.0.0.0:5000", "app:app"]
