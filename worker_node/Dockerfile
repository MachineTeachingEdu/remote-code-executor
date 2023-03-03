FROM python:3.8-slim-buster

# WORKDIR 
EXPOSE 5000
RUN echo teste
COPY requirements.txt requirements.txt
COPY src/ .
COPY bandit_config.yml .
RUN pip3 install -r requirements.txt
RUN mkdir code


CMD gunicorn \
    --max-requests-jitter 0 \
    --bind 0.0.0.0:$PORT \
    --timeout 200 \
    -w 5 \
    'server:app'