FROM python:3.12-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY scripts/run.sh ./scripts/run.sh
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
ENTRYPOINT ["/bin/sh", "/usr/src/app/scripts/run.sh"]
