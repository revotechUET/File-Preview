FROM python:3.5.8-alpine

WORKDIR /app

COPY . .

RUN apk --no-cache add libreoffice \
    ttf-droid-nonlatin \
    ttf-droid \
    ttf-dejavu \
    ttf-freefont \
    ttf-liberation \
    && rm -rf /var/cache/apk/* \
    && pip install -r requirements.txt \
    && mkdir -p uploads \
    && apk add wkhtmltopdf

ENV BUDGET_URL=https://users.i2g.cloud
ENV SERVICE=WI_PROJECT_STORAGE
ENV MPP_SERVICE_URL=http://192.168.1.15:8080

EXPOSE 5000

CMD ["python", "app.py", "-p 5000"]