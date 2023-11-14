FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

COPY ./ ./

RUN sed -i 's@archive.ubuntu.com@kr.archive.ubuntu.com@g' /etc/apt/sources.list

RUN apt update && apt install -y python3.8 \
	python3-dev \
	python3-pip \
	git

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install -r ./requirements.txt

WORKDIR /root
RUN echo 'alias python=python3.8' >> .bashrc

WORKDIR /