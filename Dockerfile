FROM python:3.12

WORKDIR /

COPY ./ /app


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["python3", "app/main.py"]