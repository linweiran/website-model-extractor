def sixdigit(n):
	strn=str(n)
	lenn=len(strn)
	if lenn<6 :
		strn= (6-lenn)*"0"+strn
	return strn

import os
import sys
import subprocess
import dpkt
sitenumber=int(sys.argv[1])
instancenumber=int(sys.argv[2])
namemode=sys.argv[3]
datamode=sys.argv[4]
source=sys.argv[5]
path="batch"
if not(os.path.isdir(path)):
	command="mkdir "+path
	subprocess.call(command.split())

for filecounter in range(sitenumber):
	for round in range(instancenumber):
		website="s"+sixdigit(filecounter)+"_"+sixdigit(round)
		print website		
		#incomecounter=0
		tcpcounter=0
		pcapfile=open(source+"/"+website+".pcap",'r')
		if namemode == "test":
			target=open("batch/"+str(filecounter*instancenumber+round),'w')
		if namemode == "learn":
			if datamode=="knn":
				target=open("batch/"+str(filecounter)+"-"+str(round),'w')
			if datamode=="kfp":
				target=open("batch/"+str(filecounter)+"_"+str(round),'w')

		for ts, pkt in dpkt.pcap.Reader(pcapfile):
			eth=dpkt.ethernet.Ethernet(pkt)
			if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
				continue
			ip=eth.data
			if ip.p==dpkt.ip.IP_PROTO_TCP: 
				tcp=ip.data
				if tcp.dport == 53 or tcp.sport == 53:
					continue    # ignore DNS
				if len(tcp.data)>0:
					if tcpcounter==0:	
						tm=ts
						threshold=eth.src
						tcpcounter+=1
					if threshold==eth.src:
						if datamode=="knn":
							target.write("{} {}\n".format(ts-tm, len(tcp.data)))
						if datamode=="kfp":
							target.write("{} {}\n".format(ts-tm, 1.0))
					else:
						if datamode=="knn":
							target.write("{} {}\n".format(ts-tm, -len(tcp.data)))
						if datamode=="kfp":
							target.write("{} {}\n".format(ts-tm, -1.0))
						#incomecounter+=1
		target.close()
		pcapfile.close()
