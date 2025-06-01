# Usa uma imagem Python enxuta
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copia e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY app.py .

# Expor a porta 5001
EXPOSE 5001

# Start com gunicorn na porta 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
