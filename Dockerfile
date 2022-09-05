FROM ubuntu:22.04
LABEL maintainer="Oleksii Leonov <mail@oleksiileonov.com>"

ENV PATH="${PATH}:/root/.local/bin"
WORKDIR /workspace
VOLUME /workspace
COPY . /workspace

RUN ( \
  export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      build-essential \
      python3.10 \
      python3.10-dev \
      python3.10-venv \
      libgsl-dev \
  && rm -rf /var/lib/apt/lists/* \
  && curl -sSL https://install.python-poetry.org | python3 - \
  && poetry install --only main --no-interaction --no-ansi \
  )

CMD [ "./run.sh" ]
