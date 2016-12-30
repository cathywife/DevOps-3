FROM ubuntu:14.04
COPY sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y openjdk-7-jdk git wget
RUN ln -fs /usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java /etc/alternatives/java
RUN mkdir -p /usr/local/vertx && cd /usr/local/vertx && \
wget http://dl.bintray.com/vertx/downloads/vert.x-2.1.2.tar.gz -qO -|tar -xz
ENV PATH /usr/local/vertx/vert.x-2.1.2/bin:$PATH
RUN mkdir -p /usr/local/src
WORKDIR /usr/local/src
CMD ["bash"]
