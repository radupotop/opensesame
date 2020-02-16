# Builder
FROM python:3.8.1-slim AS builder
RUN apt-get update && apt-get -y install gcc iptables
COPY . /app
WORKDIR /app
RUN pip wheel . -w /wheels/


# Runner
FROM python:3.8.1-slim
RUN apt-get update && apt-get -y install iptables
COPY . /app
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install /wheels/*
CMD python utils/bootstrap.py && python app/run.py
EXPOSE 8080
