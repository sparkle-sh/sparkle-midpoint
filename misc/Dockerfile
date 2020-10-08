FROM ubuntu:latest

RUN add-apt-repository ppa:deadsnakes/ppa
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN apt-get update && apt-get install -y \ 
    software-properties-common sudo tmux vim wget curl lsof psmisc

WORKDIR /sparkle-midpoint/
COPY . /sparkle-midpoint/

RUN yes | ./bin/deps.sh
RUN yes | ./bin/venv.sh

EXPOSE 7776