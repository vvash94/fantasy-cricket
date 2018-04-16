FROM alpine:3.7

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN pip install requests pymongo

RUN mkdir /score-updater

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
COPY ./update-scores.py /score-updater/update-scores.py

ENTRYPOINT ["./docker-entrypoint.sh"]
