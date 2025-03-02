# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.2
FROM python:${PYTHON_VERSION}-slim as base

# Impede a criação de arquivos .pyc e desativa buffering do stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Cria um usuário não privilegiado para rodar a aplicação
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Instala as dependências listadas no requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Altera para o usuário não privilegiado
USER appuser

# Copia o código da aplicação para o container
COPY . .

# Expondo a porta 8000
EXPOSE 8000

# Inicia a aplicação com gunicorn utilizando o worker do uvicorn
CMD gunicorn Webhook:app --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker
# CMD streamlit run app_streamlit.py --server.port=8000 --server.address=0.0.0.0
