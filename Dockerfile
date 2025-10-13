FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install-deps
RUN playwright install

COPY . .

CMD [ "python", "main.py"]