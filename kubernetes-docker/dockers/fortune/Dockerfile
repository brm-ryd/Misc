FROM alpine:latest

RUN apk --update add ; apk add fortune
ADD gen-fortune.sh /bin/gen-fortune.sh
ENTRYPOINT /bin/gen-fortune.sh
