//snippet function to generate password

#include <string.h>

static char *pass_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
"ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*( )"
"-=_+;[ ]{ }\\|,./<>?;";

char *pass_generate(char *buff, size_t bufsize) {
	size_t choices, n;
	choices = strlen(pass_chars) - 1;
	for (n = 0; n < bufsize - 1; n++) /* terminate NULL */
		buff[n] = pass_chars[spc_rand_range(0, choices)];
	buff[bufsize - 1] = 0;
	return buff;
}
