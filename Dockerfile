FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements-deploy.txt .
RUN pip install --no-cache-dir -r requirements-deploy.txt
COPY gateway ./gateway
COPY scripts ./scripts
# Public demo defaults: synthetic data only, self-serve keys, admin routes off, state in /data.
ENV SKBGW_HOME=/data SKBGW_DEMO=1 SKBGW_DISABLE_ADMIN=1
RUN useradd -m app && mkdir /data && chown app /data
USER app
EXPOSE 8000
CMD ["python", "-m", "gateway", "serve"]
