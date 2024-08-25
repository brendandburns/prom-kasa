FROM python:3-alpine

RUN pip3 install python-kasa
RUN pip3 install prometheus-client
RUN pip3 install prometheus-async

COPY prom_kasa.py /prom_kasa.py