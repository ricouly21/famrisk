FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./app/requirements.txt .

RUN echo "Installing python dependencies ..." \
    && python -m pip install --upgrade pip \
    && python -m pip install -r ./requirements.txt \
    #&& python -m pip install django djangorestframework pytz requests psycopg2-binary \
    #&& python -m pip freeze > ./requirements.txt \
    && echo "Done!"

COPY ./app /app

EXPOSE 8000

CMD ["tail", "-f", "/dev/null"]

