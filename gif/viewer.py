import sys
rfile=sys.argv[1]
with open(rfile,"r") as pf:
	hexlist=["{:02x}".format(ord(c)) for c in pf.read()]
print hexlist