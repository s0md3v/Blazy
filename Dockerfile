FROM python:2.7

WORKDIR /home
RUN mkdir Blazy
ADD . /home/Blazy
WORKDIR /home/Blazy
RUN pip install -r requirements.txt

ENTRYPOINT python blazy.py