FROM python:alpine

WORKDIR /usr/src/app

COPY ./server/server.py ./
EXPOSE 11100

CMD [ "python", "./server.py" ]
