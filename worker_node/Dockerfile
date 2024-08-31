FROM python:3.8-slim-buster

# WORKDIR 
EXPOSE 5000

#Dependências para C e Julia
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-1.9.0-linux-x86_64.tar.gz | tar -xz -C /usr/local && \
    ln -s /usr/local/julia-1.9.0/bin/julia /usr/local/bin/julia

#RUN echo teste
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