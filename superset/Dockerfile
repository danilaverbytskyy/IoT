FROM apache/superset:latest

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Install pip into Superset's venv, then install the driver in the same venv
RUN curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py \
 && /app/.venv/bin/python /tmp/get-pip.py \
 && rm -f /tmp/get-pip.py \
 && /app/.venv/bin/pip install --no-cache-dir psycopg2-binary

USER superset