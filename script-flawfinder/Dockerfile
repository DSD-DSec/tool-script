FROM alpine:3.16

RUN apk update
RUN apk add python3
RUN apk add git
RUN python3 -m ensurepip
RUN pip3 install flask
RUN pip3 install pycryptodomex
RUN pip3 install flawfinder
COPY main.py /home/app.py
COPY util.py /home/util.py
WORKDIR /home
ENTRYPOINT ["python3"]
CMD ["app.py"]
