FROM python:3.11.10-bullseye

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Comando para criar a imagem do projeto
# $ docker build -t lucasouzamil/projeto-api-consulta-dolar:v1.0 .

# Comando para publicar o projeto no Docker Hub
# $ docker push lucasouzamil/projeto-api-consulta-dolar:v1.0