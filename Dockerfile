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
        && mkdir -p uploads

ENV BUDGET_URL=https://users.i2g.cloud
ENV SERVICE=WI_PROJECT_STORAGE

EXPOSE 5000

CMD ["gunicorn", "-b 0.0.0.0:5000", "app:app"]
