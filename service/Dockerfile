FROM ubuntu:20.04

RUN apt-get update && apt-get autoremove -y && apt-get install -y \
    python3.8 \
    python3-pip \
    && apt-get clean

ENV FLASK_DEBUG=0

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

ADD . /service
WORKDIR /service

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:8000/ || exit 1
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers=1", "--timeout=120", "service"]
