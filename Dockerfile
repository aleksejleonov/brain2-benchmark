FROM ubuntu:22.04
LABEL maintainer="Oleksii Leonov <mail@oleksiileonov.com>"

RUN ( \
  export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install -y \
      build-essential \
      python3 \
      python3-pip \
      libgsl-dev \
  && mkdir /workspace \
  )

WORKDIR /workspace
VOLUME /workspace

COPY requirements.txt /workspace
RUN pip3 install -r requirements.txt

COPY benchmark/. /workspace

CMD [ "./run.sh" ]
