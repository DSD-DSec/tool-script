FROM php:8.2-alpine

USER root

RUN apk update

RUN apk add python3

RUN apk add git

RUN python3 -m ensurepip

RUN pip3 install flask

RUN pip3 install pycryptodomex

WORKDIR /home

RUN wget https://github.com/designsecurity/progpilot/releases/download/v1.0.0/progpilot_v1.0.0.phar

RUN chmod +x progpilot_v1.0.0.phar

RUN mv progpilot_v1.0.0.phar /usr/local/bin/progpilot

COPY main.py /home/app.py

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
