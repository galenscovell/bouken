FROM python:3.8.1

COPY . .

RUN apt-get update

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install

EXPOSE 8080
CMD [ "pipenv", "run", "python", "src/app.py" ]