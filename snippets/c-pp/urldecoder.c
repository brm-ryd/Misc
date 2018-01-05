//URL decoder
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define BASE16_TO_10(x) (((x) >= '0' && (x) <= '9') ? ((x) - '0') : \
	(toupper((x)) - 'A' + 10))
	
char *url_decode(const char *url, size_t *nbytes) {
	char *out, *ptr;
	const char *c;
	if (!(out = ptr = strdup(url))) return 0;
	for (c = url; *c; c++) {
		if (*c != '%' || !isxdigit(c[1]) || !isxdigit(c[2])) *ptr++ = *c;
		else {
			*ptr++ = (BASE16_TO_10(c[1]) * 16) + (BASE16_TO_10(c[2]));
			c += 2;
		}
	}
	*ptr = 0;
	if (nbytes) *nbytes = (ptr - out); /* not include null byte */
	return out;
}
