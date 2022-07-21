FROM python:3.8-slim as devo

MAINTAINER Soubhagya R Nayak <soubhagya.r.nayak@gmail.com>

#RUN apk update && apk add build-base postgresql-dev libffi-dev libcurl curl-dev

RUN apt-get update && apt-get install apt-file -y && apt-file update
RUN apt-get install -y libssl-dev libcurl4-openssl-dev gcc libpq-dev

COPY requirements.txt requirements.txt
RUN pip install --user --requirement requirements.txt
RUN pip install --user psycopg2-binary

COPY ./newsparser /root/.local/newsparser

FROM python:3.7-slim

COPY --from=devo /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

CMD ["python","/root/.local/newsparser/task_processor.py"]
