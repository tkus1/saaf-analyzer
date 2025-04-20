FROM apache/superset

USER root
COPY docker-init.sh /app/docker-init.sh
RUN chmod +x /app/docker-init.sh

RUN apt update && apt install -y curl unzip \
    && curl -LO https://github.com/duckdb/duckdb/releases/download/v1.2.2/duckdb_cli-linux-aarch64.zip \
    && unzip duckdb_cli-linux-aarch64.zip -d /usr/local/bin \
    && chmod +x /usr/local/bin/duckdb \
    && rm duckdb_cli-linux-aarch64.zip

RUN pip install duckdb-engine

USER superset
ENTRYPOINT ["/app/docker-init.sh"]