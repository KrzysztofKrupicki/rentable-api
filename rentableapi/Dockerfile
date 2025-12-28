FROM python:3.13-alpine3.20

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r ./requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /src
COPY ./src /src

RUN adduser -D user
USER user

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
