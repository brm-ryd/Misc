//simple chain lookup using gethostbyname
//clookup.c
//clookup hostname1 hostname2 hostname3

#include <stdio.h>
#include<unistd.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

extern int h_errno;

int main(int argc, char **argv)
{
  int i, i1;
  struct hostent *hp;
  for(i=1;i<argc; ++i)
  {
    hp = gethostbyname(argv[i]);
    if(!hp)
    {
      fprintf(stderr, "%s: host '%s'\n", hstrerror(h_errno), argv[i]);
      continue;
    }

    printf("host %s : \n", argv[i]);
    printf(" Officially:\t%s\n", hp->h_name);
    fputs(" Aliases:\t", stdout);
    for(i1=0; hp->h_aliases[i1]; ++i1)
    {
      if(i1)
        fputs(", ", stdout);
      fputs(hp->h_aliases[i1], stdout);
    }
    fputc("\n", stdout);
    printf("  Type:\t\t%s\n", hp->h_addrtype == AF_INET ? "AF_INET":"AF_INET6");
    if(hp->h_addrtype == AF_INET)
     {
       for(i1=0;hp->h_addr_list[i1];++i1)
	 printf("  Address:\t%s\n", inet_ntoa( *(struct in_addr *) hp->h_addr_list[i1]));
     }
     putchar("\n");
  }
  return 0;
}
