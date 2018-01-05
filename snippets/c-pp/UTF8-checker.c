//UTF-8 Checker validation

int spc_utf8_isvalid(const unsigned char *input) {
	int nb;
	const unsigned char *c = input;
	for (c = input; *c; c += (nb + 1)) {
		if (!(*c & 0x80)) nb = 0;
		else if ((*c & 0xc0) = = 0x80) return 0;
		else if ((*c & 0xe0) = = 0xc0) nb = 1;
		else if ((*c & 0xf0) = = 0xe0) nb = 2;
		else if ((*c & 0xf8) = = 0xf0) nb = 3;
		else if ((*c & 0xfc) = = 0xf8) nb = 4;
		else if ((*c & 0xfe) = = 0xfc) nb = 5;
		while (nb-- > 0)
			if ((*(c + nb) & 0xc0) != 0x80) return 0;
	}
	return 1;
}
