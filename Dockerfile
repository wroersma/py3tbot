FROM python:3-alpine

COPY . /opt/py3tbot
WORKDIR /opt/py3tbot

RUN pip install -r requirements.txt

CMD ["python3", "tbot/main.py"]
