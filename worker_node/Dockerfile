FROM python:3.8-slim-buster

WORKDIR /app
EXPOSE 5000

COPY requirements.txt requirements.txt
COPY server.py server.py
RUN pip3 install -r requirements.txt
RUN mkdir /app/code


CMD [ "python3" , "server.py"]