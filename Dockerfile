FROM python:3.10-slim

ADD . /opt/discord
WORKDIR /opt/discord

RUN pip install -r ./requirements.txt

CMD python ./core/main.py