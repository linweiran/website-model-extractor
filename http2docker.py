import os
import sys
import subprocess
times=int(sys.argv[1])
mode=sys.argv[2]
httppath="http-"+mode
Caddypath="Caddy-"+mode
path="data"
if not(os.path.isdir(path)):
	command="mkdir "+path
	subprocess.call(command.split())
if not(os.path.isdir(path+"/pcap")):
	command="mkdir "+path+"/pcap"
	subprocess.call(command.split())
inputfile=open("parsed.txt","r")
unparsedsites= inputfile.readlines()

sites=[]
maxwindow=20
while len(unparsedsites)>0:
	sites.append(unparsedsites.pop(0).strip())
	if (len(sites)==maxwindow) or (len(unparsedsites)==0):
		try:
			networkstart={}
			for website in sites:
				print "starting network "+website+"..............."
				networkstartcommand="docker network create "+website
				networkstart[website]=subprocess.Popen(networkstartcommand.split())
			for website in sites:
				networkstart[website].wait()
				print "network "+website+" created***************"
			try:	
				image={}
				for website in sites:
					rwebsite=website.replace(".","_")
					print "docker image "+website+" starting###############"
					imagecommand="docker run --rm --name "+rwebsite+"-caddy.ttat.xyz --net "+website+" -v "+os.path.abspath(".")+"/"+Caddypath+"/"+website+"-Caddyfile:/etc/Caddyfile -v /home/nikita/caddy/ttat.xyz:/certs -v "+os.path.abspath(".")+"/"+httppath+"/"+website+":/srv abiosoft/caddy"
					image[website]=subprocess.Popen(imagecommand.split())
				for step in range(0,times):
					print "current cycle:"+str(step)+ "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
					crawler={}
					for website in sites:
						rwebsite=website.replace(".","_")
						crawlercommand="docker run --net "+website+" --rm -v "+os.path.abspath("./data")+":/data nikitab/devtoolcrawler:tcpdump --pcap --no-mysql -p https:// -s "+rwebsite+"-caddy.ttat.xyz"
						print website+" loading///////////////"
						crawler[website]=subprocess.Popen(crawlercommand.split())
					for website in sites:
						rwebsite=website.replace(".","_")
						crawler[website].wait()
						print website+" moving|||||||||||||||"
						list=os.listdir(path)
						for directory in list:
							if rwebsite+"-" in directory:
								command = "mv "+path+"/"+directory+"/"+rwebsite+"-caddy.ttat.xyz.pcap "+path+"/pcap/"+website+"_"+str(step)+".pcap"
								subprocess.call(command.split())
								command = "rm -r "+path+"/"+directory
								subprocess.call(command.split())
		
			finally:
				for website in sites:
					print "terminating docker image "+website+" %%%%%%%%%%%%%%%"
					image[website].terminate()
				for website in sites:
					image[website].wait()
					print "docker image "+website+"terminated---------------"
		finally:
			networkend={}
			for website in sites:
				networkendcommand="docker network rm "+website
				networkend[website]=subprocess.Popen(networkendcommand.split())
				print "ending network "+website+" ^^^^^^^^^^^^^^^"
			for website in sites:
				networkend[website].wait()
				print "network "+website+" ended :::::::::::::::"
		sites=[]