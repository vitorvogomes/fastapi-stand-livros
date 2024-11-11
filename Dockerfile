FROM python:3.12.3
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY wait_for_it.sh /wait_for_it

COPY . .

CMD [ "/wait_for_it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
