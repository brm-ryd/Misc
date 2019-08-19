FROM golang:1.11-alpine AS build

WORKDIR /source/
COPY main.go go.* /source/

RUN CGO_ENABLED=0 go build -0 /bin/test1

FROM scratch
COPY --from=build /bin/test1 /bin/test1
ENTRYPOINT [ "/bin/test1" ]