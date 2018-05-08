FROM	alpine

RUN	apk	update
RUN	apk	upgrade

RUN	apk	add	python3

#	make	a	directory	for	our	application
RUN	mkdir	-p	/opt/exampleapp

#	move	requirements	file	into	the	container
COPY	.	/opt/exampleapp/

#	install	the	library	dependencies	for	this	application
RUN	pip3	install	-r	/opt/exampleapp/requirements.txt
ENTRYPOINT	["python3"]
CMD	["/opt/exampleapp/exampleapp.py"]
