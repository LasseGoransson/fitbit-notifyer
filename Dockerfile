FROM python:3

ADD fitbit-notify.py /script.py
ADD config.yml       /config.yml

RUN pip install python-pushover fitbit schedule pyyaml

CMD [ "python", "./script.py" ]
 
