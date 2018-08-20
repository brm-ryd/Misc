FROM golang:alpine

ENV gopath /codes/
ADD . /codes/repos/golang/monitoring/
WORKDIR /codes/repos/golang/monitoring/
RUN go build

ENTRYPOINT /codes/repos/golang/monitoring/
