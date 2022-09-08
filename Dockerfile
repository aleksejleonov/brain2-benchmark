FROM python:3.10.6-bullseye
LABEL maintainer="Oleksii Leonov <mail@oleksiileonov.com>"

WORKDIR /workspace
VOLUME /workspace
COPY . /workspace
RUN pip3 install -r requirements.txt

CMD [ "./run.sh" ]
