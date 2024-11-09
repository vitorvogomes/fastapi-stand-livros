FROM python:3.6.9
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Baixe o entrypoint.sh diretamente durante o build
RUN curl -o entrypoint.sh https://raw.githubusercontent.com/vishnubob/entrypoint/master/entrypoint.sh && \
    chmod +x entrypoint.sh

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
