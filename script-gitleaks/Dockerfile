FROM zricethezav/gitleaks:latest

USER root
RUN apk update
RUN apk add python3
RUN python3 -m ensurepip
RUN pip3 install flask
RUN pip3 install pycryptodomex
COPY script-gitleaks/main.py /home/app.py
COPY util.py /home/util.py
WORKDIR /home
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
