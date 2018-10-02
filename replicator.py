import sys
import subprocess
import time
import os
from pathlib import Path

if not os.path.isdir("http-replica"):
	mkdir="mkdir http-replica"
	subprocess.call(mkdir.split())
inputfile=open("parsed.txt","r")
sites = inputfile.readlines()



dockerhead="docker run -p 80:80 --rm -v /home/wlin40/website-model-extractor/"
dockertail=":/usr/local/apache2/htdocs:ro httpd"
reproduce="python3 reproduce.py"
mvdir="mv ttat.json "

for times in range(1,int(sys.argv[1])+1):
	for website in sites:
		website=website.strip()

		readfrom="http-off/"+website
		writeto='http-replica/' + website +"-"+str(times)+ '.json'
		if Path(writeto).exists():
			continue
		dockercommand=dockerhead+readfrom+dockertail
		docker=subprocess.Popen(dockercommand.split())
		reproducer=subprocess.call(reproduce.split())
		docker.terminate()
		docker.wait()
		mvcommand=mvdir+writeto
		mvd=subprocess.call(mvcommand.split())
		time.sleep(1)