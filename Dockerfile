FROM python:3

WORKDIR /app

RUN pip install python-pushover fitbit schedule pyyaml

CMD [ "python", "/app/fitbit-notify.py" ]
 
