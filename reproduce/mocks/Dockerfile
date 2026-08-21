FROM python:3.12-slim
WORKDIR /app
COPY mocks/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY inventory.py /app/inventory.py
COPY mocks/app.py /app/app.py
ENV PYTHONPATH=/app
EXPOSE 8088
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8088"]
