# Import modules for CGI handling
import cgi, cgitb
import ntop, interface, json

# Parse URL
cgitb.enable();

form = cgi.FieldStorage();
name = form.getvalue('Name', default="nubie")

version = ntop.version()
os = ntop.os()
uptime = ntop.uptime()

ifnames = []
try:
    for i in range(interface.numInterfaces()):
        ifnames.append(interface.name(i))

except Exception as inst:
    print type(inst) # the exception instance
    print inst.args # arguments stored in .args
    print inst # __str__ allows args to printed directly


ntop.printHTMLHeader('Test Mininet NTOP Env', 1, 0)
ntop.sendString("Hello, "+ name +"<br>")
ntop.sendString("Ntop Information: %s %s %s" % (version, os, uptime))
ntop.sendString("Here are my interfaces: <br>")
ntop.sendString(json.dumps(ifnames, sort_keys=True, indent=4))
ntop.printHTMLFooter()
