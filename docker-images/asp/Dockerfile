FROM python:3.11-slim

RUN apt-get update && apt-get install -y iputils-ping

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV IS_RUNNING_IN_DOCKER=True

CMD ["python", "-u", "asp.py"]