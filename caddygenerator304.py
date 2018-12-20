def sixdigit(n):
	strn=str(n)
	lenn=len(strn)
	if lenn<6 :
		strn= (6-lenn)*"0"+strn
	return strn

import os
import subprocess
import sys

path="Caddy"
if not(os.path.isdir(path)):
	command="mkdir "+path
	subprocess.call(command.split())
dir=sys.argv[1]
sitenum=int(sys.argv[2])
instancenum=int(sys.argv[3])
for i in range(sitenum):
	for j in range(instancenum):

		website="s"+sixdigit(i)+"_"+sixdigit(j)

		with open(path+"/"+website+"-Caddyfile","w") as f:
			line1=website+"-caddy.ttat.xyz:443 {"
			line2="  tls /certs/fullchain1.pem /certs/privkey1.pem"
			line3="  log stdout"
			line5="}"
			f.write("{}\n".format(line1))
			f.write("{}\n".format(line2))
			f.write("{}\n".format(line3))

			files=os.listdir(dir+"/"+website)
			line4="  push /"
			paddingflag=0
			for file in files:
				if file=="Xscript33.js":
					paddingflag=1
					continue
				if file<>"index.html":
					line4+=" /"+file
			if paddingflag == 1:
				line4+=" /Xscript33.js"
			if line4 <> "  push /":
				f.write("{}\n".format(line4))
	
			f.write("{}\n".format(line5))