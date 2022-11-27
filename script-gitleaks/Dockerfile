FROM zricethezav/gitleaks:latest

USER root
RUN apk update
RUN apk add python3
RUN python3 -m ensurepip
RUN pip3 install flask
COPY main.py /home/app.py
WORKDIR /home
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
