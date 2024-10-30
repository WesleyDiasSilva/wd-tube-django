FROM python:3.12.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PIPENV_VENV_IN_PROJECT 1

RUN pip install pipenv

RUN useradd -ms /bin/bash my-user

# Temporariamente muda para root para configurar permissões
USER root

# Cria o diretório de trabalho com permissões de my-user
RUN mkdir -p /media/uploads && chown -R my-user:my-user /media/uploads

# Define o diretório de trabalho como /home/my-user/app e muda o usuário para my-user
WORKDIR /home/my-user/app
USER my-user

CMD tail -f /dev/null