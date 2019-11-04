FROM python:3.5.8-alpine

WORKDIR /app

ENV BUDGET_URL=https://users.i2g.cloud
ENV SERVICE=WI_PROJECT_STORAGE

COPY . .

RUN apk --no-cache add libreoffice \
        && rm -rf /var/cache/apk/* \
        && pip install -r requirements.txt \
        && mkdir -p uploads

EXPOSE 5000

CMD ["gunicorn", "-b 0.0.0.0:5000", "app:app"]
