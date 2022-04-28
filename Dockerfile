FROM python:3.10-slim
WORKDIR /code

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
build-essential gcc 

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /code/src
EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]