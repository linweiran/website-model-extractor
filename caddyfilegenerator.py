import os
import subprocess
import sys

path="Caddy"
if not(os.path.isdir(path)):
	command="mkdir "+path
	subprocess.call(command.split())
inputfile=open("parsed.txt","r")
unparsedsites= inputfile.readlines()
dir=sys.argv[1]
for site in unparsedsites:
		website=site.strip()
		rwebsite=website.replace(".","_")
		with open(path+"/"+website+"-Caddyfile","w") as f:
			line1=rwebsite+"-caddy.ttat.xyz:443 {"
			line2="  tls /certs/fullchain1.pem /certs/privkey1.pem"
			line3="  log stdout"
			line5="}"
			f.write("{}\n".format(line1))
			f.write("{}\n".format(line2))
			f.write("{}\n".format(line3))

			files=os.listdir(dir+"/"+website)
			line4="  push /"
			for file in files:
				if file<>"index.html":
					line4+=" /"+file
			if line4 <> "  push /":
				f.write("{}\n".format(line4))
	
			f.write("{}\n".format(line5))