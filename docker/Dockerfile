# Builder
FROM python:3.8.2-slim AS builder
RUN apt-get update && apt-get -y install gcc iptables
COPY . /app
WORKDIR /app
RUN pip wheel . -w /wheels/


# Runner
FROM python:3.8.2-slim
RUN apt-get update && apt-get -y install iptables
COPY --from=builder /wheels /wheels
RUN pip install /wheels/*
COPY . /app
WORKDIR /app
CMD python utils/bootstrap.py && python app/run.py
EXPOSE 8080
