FROM python:3.11.0a5-alpine

RUN adduser -D junglepy

WORKDIR /home/junglepy

COPY requirements.txt requirements.txt
RUN apk add --update py-pip
RUN python -m venv venv
RUN apk add build-base
RUN venv/bin/pip3 install -r requirements.txt
RUN venv/bin/pip3 install gunicorn

COPY app app
COPY web.py config.py vacs.db boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP web.py

RUN chown -R junglepy:junglepy ./
USER junglepy

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]