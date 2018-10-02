def sixdigit(n):
	strn=str(n)
	lenn=len(strn)
	if lenn<6 :
		strn= (6-lenn)*"0"+strn
	return strn

import os
import sys
import subprocess


sitenumber=int(sys.argv[1])
instancenumber=int(sys.argv[2])

unparsedsites=[]
for i in range(sitenumber):
	for j in range(instancenumber):
		website="s"+sixdigit(i)+"_"+sixdigit(j)
		unparsedsites.append(website)

mode="off"
httppath="http-"+mode
Caddypath="Caddy-"+mode
path="data"
if not(os.path.isdir(path)):
	command="mkdir "+path
	subprocess.call(command.split())
if not(os.path.isdir(path+"/pcap")):
	command="mkdir "+path+"/pcap"
	subprocess.call(command.split())



sites=[]
maxwindow=20
while len(unparsedsites)>0:
	sites.append(unparsedsites.pop(0))
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
					print "docker image "+website+" starting###############"
					imagecommand="docker run --rm --name "+website+"-caddy.ttat.xyz --net "+website+" -v "+os.path.abspath(".")+"/"+Caddypath+"/"+website+"-Caddyfile:/etc/Caddyfile -v /home/nikita/caddy/ttat.xyz:/certs -v "+os.path.abspath(".")+"/"+httppath+"/"+website+":/srv abiosoft/caddy"
					image[website]=subprocess.Popen(imagecommand.split())



				print "current cycle:preparing"+ "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
				crawler={}
				for website in sites:
					crawlercommand="docker run --net "+website+" --rm -v "+os.path.abspath("./data")+":/data nikitab/devtoolcrawler:tcpdump --pcap --no-mysql -p https:// -s "+website+"-caddy.ttat.xyz"
					crawler[website]=subprocess.Popen(crawlercommand.split())
				for website in sites:
					crawler[website].wait()
					list=os.listdir(path)
					for directory in list:
						if website+"-" in directory:
							command = "rm -r "+path+"/"+directory
							subprocess.call(command.split())




				print "current cycle:loading"+ "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
				crawler={}
				for website in sites:
					crawlercommand="docker run --net "+website+" --rm -v "+os.path.abspath("./data")+":/data nikitab/devtoolcrawler:tcpdump --pcap --no-mysql -p https:// -s "+website+"-caddy.ttat.xyz"
					print website+" loading///////////////"
					crawler[website]=subprocess.Popen(crawlercommand.split())
				for website in sites:
					crawler[website].wait()
					print website+" moving|||||||||||||||"
					list=os.listdir(path)
					for directory in list:
						if website+"-" in directory:
							command = "mv "+path+"/"+directory+"/"+website+"-caddy.ttat.xyz.pcap "+path+"/pcap/"+website+".pcap"
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