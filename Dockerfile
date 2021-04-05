FROM python:3-buster

RUN pip3 install python-kasa
RUN pip3 install prometheus-client
COPY smartstrip-hacked.py /usr/local/lib/python3.9/site-packages/kasa/smartstrip.py

COPY prom_kasa.py /prom_kasa.py