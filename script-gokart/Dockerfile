FROM golang:1.19-alpine

RUN apk update
RUN apk add python3
RUN apk add git
RUN python3 -m ensurepip
RUN pip3 install flask
RUN pip3 install pycryptodomex
RUN go install github.com/praetorian-inc/gokart@latest
COPY util.py /home/util.py
COPY main.py /home/app.py
WORKDIR /home
ENTRYPOINT ["python3"]
CMD ["app.py"]
