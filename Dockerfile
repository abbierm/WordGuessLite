FROM python:3.13

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY gameplay /code/gameplay
COPY routers /code/routers
COPY words /code/words
COPY dependencies.py main.py /code/

CMD ["fastapi", "run", "main.py", "--port", "80", "--workers", "4"]