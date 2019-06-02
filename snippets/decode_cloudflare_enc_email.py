#!/usr/bin/python3
"""
decrypt protected email obfuscation cloudflare
__cf_email__ tag in website data_email (web inspector / debugger)
"""

def decodeEmail(e):
    de = ""
    k = int(e[:2],16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2],16)^k)

    return de

print(decodeEmail("521637213b3e3b333c2b123b3c3f33202133267c313d3f"))

""""
(function () {
    try {
        var s, a, i, j, r, c, l = document.getElementById("__cf_email__");
        a = l.className;
        if (a) {
            s = '';
            r = parseInt(a.substr(0, 2), 16);
            for (j = 2; a.length - j; j += 2) {
                c = parseInt(a.substr(j, 2), 16) ^ r;
                s += String.fromCharCode(c);
            }
            s = document.createTextNode(s);
            l.parentNode.replaceChild(s, l);
        }
    } catch (e) {}
})();
"""
