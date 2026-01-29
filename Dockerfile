FROM ubuntu:latest
LABEL authors="yuta"

ENTRYPOINT ["top", "-b"]