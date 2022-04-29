FROM python:3.10-slim
WORKDIR /backend

RUN apt-get update

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /backend
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]