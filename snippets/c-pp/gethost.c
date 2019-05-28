/* gethost.c */
/* lookup hostname */

#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>


int main(int argc, char *argv[])
{
	struct hostent *buf;
	struct in_addr **paddr;
	char **palias;
	
	if(argc != 2) {
		puts("gethost <host name>");
		exit(EXIT_FAILURE);
	}
	
	if ((buf = gethostbyname(argv[1])) == NULL)
		// herr_quit("gethostbyname");
		return 1;
	printf("host information %s\n", argv[1]);
	printf("name: %s\n", buf->h_name);
	puts("ALIAS: ");
	palias = buf->h_aliases;
	while(*palias) {
		printf("\t%s\n", *palias);
		palias++;
	}
	
	if (buf->h_addrtype == AF_INET)
		puts("type: AF_INET");
	else
		puts("type: unknown");
	printf("length: %d\n", buf->h_length);
	puts("address: ");
	paddr = (struct in_addr **)buf->h_addr_list;
	while(*paddr) {
		printf("\t%s\n", inet_ntoa(**paddr));
		paddr++;
	}
	exit(EXIT_SUCCESS);
}
