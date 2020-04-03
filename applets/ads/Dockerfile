FROM python:3.8-buster

# Add files
COPY app /app
RUN pip install --no-cache-dir -r /app/requirements.txt  #

CMD ["python", "/app/requirements.txt"]
