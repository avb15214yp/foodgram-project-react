FROM python:3.7-slim

WORKDIR /app/foodgram

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .
COPY static/ingredients.csv .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]