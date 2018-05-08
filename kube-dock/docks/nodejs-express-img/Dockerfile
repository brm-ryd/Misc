FROM	alpine

RUN	apk	update
RUN	apk	upgrade
RUN	apk	add	nodejs	nodejs-npm

#	make	a	directory	for	our	application
WORKDIR	/src

#	move	requirements	file	into	the	container
COPY	package.json	.
COPY	package-lock.json	.

#	install	the	library	dependencies	for	this	application
RUN	npm	install	--production

#	copy	in	the	rest	of	our	local	source
COPY	.	.

#	set	the	debug	environment	variable
ENV	DEBUG=kfd-nodejs:*
CMD	["npm",	"start"]
