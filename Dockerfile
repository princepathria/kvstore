FROM python:3.8-alpine
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
COPY kv_store.py .
CMD python kv_store.py --server
