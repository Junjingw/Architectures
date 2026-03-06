FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
# Keep the container running or override with CMD in compose
CMD ["python"]

