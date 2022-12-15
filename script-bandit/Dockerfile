FROM alpine:3.16

USER root
RUN apk update
RUN apk add python3
RUN apk add git
RUN python3 -m ensurepip
RUN pip3 install flask
RUN pip3 install pycryptodomex
RUN pip3 install bandit
COPY script-bandit/main.py /home/app.py
COPY util.py /home/util.py
WORKDIR /home
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
