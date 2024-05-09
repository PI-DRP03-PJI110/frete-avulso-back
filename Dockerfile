# Use a imagem base do Python
FROM python:3.12.3-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Copia todo o conteúdo do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Define a porta em que o contêiner estará escutando
EXPOSE 8080

# Define o comando padrão para executar quando o contêiner é iniciado
ENV FLASK_APP=app.py
CMD ["waitress-serve", "--listen=0.0.0.0:8080", "--call", "app:run"]
