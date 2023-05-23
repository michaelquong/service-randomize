# Application runtime
FROM python:3.8 as base

RUN groupadd mygroup &&\
    useradd -G mygroup -m myuser

RUN mkdir -p /var/opt/myapp &&\
    mkdir -p /var/opt/myapp/instance &&\
    chown -R myuser:mygroup /var/opt/myapp &&\
    chown -R myuser:mygroup /var/opt/myapp/instance

VOLUME [ "/var/opt/myapp/instance" ]

WORKDIR /var/opt/myapp

RUN apt-get update
RUN python -m pip install --upgrade pip

USER myuser

# Application libraries
FROM base as libraries

COPY requirements.txt requirements.txt
RUN python -m pip install --user -r requirements.txt


# Application Service
FROM base

COPY --from=libraries /home/myuser/.local /home/myuser/.local
ENV PATH=/home/myuser/.local/bin:$PATH

COPY run.py /var/opt/myapp/run.py
COPY entrypoint.sh /var/opt/myapp/entrypoint.sh
COPY makefile /var/opt/myapp/makefile
COPY .env /var/opt/myapp/.env
COPY migrations /var/opt/myapp/migrations
COPY app /var/opt/myapp/app

ENTRYPOINT [ "/var/opt/myapp/entrypoint.sh" ]
CMD [ "production" ]
