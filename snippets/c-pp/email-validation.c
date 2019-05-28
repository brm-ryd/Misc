//check email address syntax address
//only support this kind of format "test@test.com"
#include <string.h>
int isemail_valid(const char *address) {
	int count = 0;
	const char *c, *domain;
	static char *rfc822_chars = "()<>@,;:\\\"[]";
	
	/* validate the name email (name@domain) */
	for (c = address; *c; c++) {
		if (*c == '\"' && (c == address || *(c - 1) == '.' || *(c - 1) == '\"')) {
			while (*++c) {
				if (*c == '\"') break;
				if (*c == '\\' && (*++c == ' ')) continue;
				if (*c <= ' ' || *c >= 127) return 0;
			}
			if (!*c++) return 0;
			if (*c == '@') break;
			if (*c != '.') return 0;
			continue;	
		}
		if (*c == '@') break;
		if (*c <= ' ' || *c >= 127) return 0;
		if (strchr(rfc822_chars, *c)) return 0;
	}
	if (c == address || *(c - 1) == '.') return 0;
	
	/* domain validation */
	if (!*(domain = ++c)) return 0;
	do {
		if (*c == '.') {
			if (c == domain || *(c - 1) == '.') return 0;
			count++;
		}
		if (*c <= ' ' || *c >= 127) return 0;
		if (strchr(rfc822_chars, *c)) return 0;
	} 
	while (*++c);
	return (count >= 1);
}
