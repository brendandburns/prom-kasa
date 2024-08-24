FROM python:3-bookworm

RUN pip3 install python-kasa
RUN pip3 install prometheus-client

COPY prom_kasa.py /prom_kasa.py