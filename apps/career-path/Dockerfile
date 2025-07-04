FROM python:3.12-slim

# Instalar uv
RUN pip install --no-cache-dir uv

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de configuração
COPY pyproject.toml uv.lock* ./

# Instalar dependências
RUN uv sync --frozen

# Copiar código fonte
COPY app/ ./app/

# Expor porta
EXPOSE 5000

# Comando para executar o servidor
CMD ["uv", "run", "python", "-m", "app.server"] 