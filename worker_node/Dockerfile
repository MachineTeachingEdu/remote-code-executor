FROM python:3.8-slim-buster

# WORKDIR 
EXPOSE 5000
RUN echo teste
COPY requirements.txt requirements.txt
COPY server.py server.py
RUN pip3 install -r requirements.txt
RUN mkdir code


CMD [ "python3" , "server.py"]