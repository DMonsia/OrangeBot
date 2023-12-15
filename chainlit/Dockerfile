FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && \
    apt-get install -y wget curl tesseract-ocr && \
    apt-get clean && \
    apt-get remove --purge -y

WORKDIR /app

COPY ./public /app
COPY ./src /app
COPY ./.env /app
COPY ./chainlit.md /app
COPY ./config.py /app
COPY ./main.py /app
COPY ./requirements.txt /tmp/requirements.txt

RUN mkdir data
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -r /tmp/requirements.txt

EXPOSE 8000

CMD ["chainlit", "run", "main.py"]
