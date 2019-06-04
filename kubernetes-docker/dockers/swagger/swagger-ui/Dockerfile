FROM alpine

LABEL name=swagger-ui
#RUN apk --update add
#RUN mkdir -p /opt/java-jaxrs

#RUN git clone https://github.com/swagger-api/swagger-samples /opt/

#COPY ["/home/nubie/codes/swagger-samples/java/java-jaxrs/*","/opt/java-jaxrs/"]

#CMD ["/usr/bin/java","-version"]

#ENTRYPOINT mvn package -Dlog4j.configuration=file:./conf/log4j.properties jetty:run


# preserve Java 8  from the maven install.
#RUN mv /etc/alternatives/java /etc/alternatives/java8
#RUN apt-get update -y && apt-get install maven -y

# Restore Java 8
#RUN mv -f /etc/alternatives/java8 /etc/alternatives/java
#RUN ls -l /usr/bin/java && java -version
ENV LANG C.UTF-8

# add a simple script that can auto-detect the appropriate JAVA_HOME value
# based on whether the JDK or only the JRE is installed
#RUN { \
#		echo '#!/bin/sh'; \
#		echo 'set -e'; \
#   	echo; \
#		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
#	} > /usr/local/bin/docker-java-home \
#	&& chmod +x /usr/local/bin/docker-java-home
ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk
ENV PATH $PATH:/usr/lib/jvm/java-1.8-openjdk/jre/bin:/usr/lib/jvm/java-1.8-openjdk/bin

ENV JAVA_VERSION 8u151
ENV JAVA_ALPINE_VERSION 8.151.12-r0

# RUN set -x \
#	 && apk add --no-cache \
#		openjdk8="$JAVA_ALPINE_VERSION" \
#	&& [ "$JAVA_HOME" = "$(docker-java-home)" ]

RUN apk add --no-cache \
		openjdk8="$JAVA_ALPINE_VERSION"

# If you're reading this and have any feedback on how this image could be
# improved, please open an issue or a pull request so we can discuss it!
#
#   https://github.com/docker-library/openjdk/issues
# From this below i copy from the github files swagger-ui.
# i doubt i can make this running without read/use github content files of swagger-ui instruction
ENV VERSION "v2.2.10"
ENV FOLDER "swagger-ui-2.2.10"
#ENV API_URL "http://petstore.swagger.io/v2/swagger.json"
ENV API_URL "http://localhost:8002/api/swagger.json"
ENV API_URLS ""
ENV API_KEY "**None**"
ENV OAUTH_CLIENT_ID "**None**"
ENV OAUTH_CLIENT_SECRET "**None**"
ENV OAUTH_REALM "**None**"
ENV OAUTH_APP_NAME "**None**"
ENV OAUTH_ADDITIONAL_PARAMS "**None**"
ENV SWAGGER_JSON "/app/swagger.json"
ENV PORT 80
ENV BASE_URL ""

RUN apk add --update nginx git
RUN mkdir -p /run/nginx
RUN git clone https://github.com/swagger-api/swagger-ui /opt/
#WORKDIR /opt
#RUN mkdir -p /usr/share/nginx/html
RUN mkdir -p /usr/share/nginx/html
RUN /bin/cp /opt/nginx.conf /etc/nginx/
RUN	/bin/cp /opt/dist/* /usr/share/nginx/html/
RUN /bin/cp /opt/docker-run.sh /usr/share/nginx/

EXPOSE 80

#CMD ["/bin/sh","/usr/share/nginx/docker-run.sh"]
ENTRYPOINT /bin/sh /usr/share/nginx/docker-run.sh
