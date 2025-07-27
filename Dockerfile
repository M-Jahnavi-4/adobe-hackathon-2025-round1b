FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY main.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir input output

CMD ["python", "main.py"]
