ARG VARIANT="3.9-slim"
FROM python:${VARIANT}

ENV APP_DIR=/app

WORKDIR ${APP_DIR}

# setup python environ
COPY ./requirements.txt ${APP_DIR}

RUN pip install -r ${APP_DIR}/requirements.txt

RUN apt update \ 
    && apt install -y --no-install-recommends \
    curl \ 
    git \
    wget \
    && apt purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/cli/cli/releases/download/v2.4.0/gh_2.4.0_linux_amd64.deb \
    && dpkg -i gh_*_linux_amd64.deb \
    && rm -r gh_*_linux_amd64.deb
