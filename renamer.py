import os
import subprocess
import sys
times=int(sys.argv[1])
path="data"
if not(os.path.isdir(path)):
	command="mkdir "+path
	subprocess.call(command.split())
if not(os.path.isdir(path+"/pcap")):
	command="mkdir "+path+"/pcap"
	subprocess.call(command.split())



for step in range(0,times):
	inputfile=open("parsed.txt","r")
	sites = inputfile.readlines()
	for website in sites:
		website=website.strip()
		if os.path.exists(path+"/pcap/"+website+"_"+str(step)+".pcap"):
			continue
		command="docker run -v "+os.path.abspath("./data")+":/data nikitab/devtoolcrawler:tcpdump --pcap --no-mysql -s" +website
		
		tcpdump = subprocess.Popen(command.split())
		tcpdump.wait()

		list=os.listdir(path)
	
		for directory in list:
			if website+"-" in directory:
				command = "mv "+path+"/"+directory+"/"+website+".pcap "+path+"/pcap/"+website+"_"+str(step)+".pcap"
				subprocess.call(command.split())
				command = "rm -r "+path+"/"+directory
				subprocess.call(command.split())
