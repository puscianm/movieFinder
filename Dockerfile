FROM python:3.9

WORKDIR /app

COPY back/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "back/app.py"]
