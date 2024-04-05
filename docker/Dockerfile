FROM python:3.11.8-slim AS base
RUN apt-get update && apt-get -y install iptables

# Builder
FROM base AS builder
RUN apt-get -y install gcc
COPY requirements.txt /app/
RUN pip wheel -r /app/requirements.txt -w /wheels/

# Runner
FROM base AS runner
COPY --from=builder /wheels /wheels
RUN pip install /wheels/*
COPY . /app
WORKDIR /app
RUN pip install .
CMD python utils/bootstrap.py && python api/run.py
EXPOSE 8080
