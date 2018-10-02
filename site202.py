def gifg(n,filename):
	gifdict={}
	gifdict[0]="47"
	gifdict[1]="49"
	gifdict[2]="46"
	gifdict[3]="38"
	gifdict[4]="39"
	gifdict[5]="61"
	gifdict[6]="01"
	gifdict[7]="00"
	gifdict[8]="01"
	gifdict[9]="00"
	gifdict[10]="f0"
	gifdict[11]="00"
	gifdict[12]="00"
	gifdict[13]="9d"
	gifdict[14]="95"
	gifdict[15]="8c"
	gifdict[16]="00"
	gifdict[17]="00"
	gifdict[18]="00"
	gifdict[19]="21"
	gifdict[20]="f9"
	gifdict[21]="04"
	gifdict[22]="00"
	gifdict[23]="00"
	gifdict[24]="00"
	gifdict[25]="00"
	gifdict[26]="00"
	gifdict[27]="2c"
	gifdict[28]="00"
	gifdict[29]="00"
	gifdict[30]="00"
	gifdict[31]="00"
	gifdict[32]="01"
	gifdict[33]="00"
	gifdict[34]="01"
	gifdict[35]="00"
	gifdict[36]="00"
	gifdict[37]="02"
	gifdict[38]="02"
	gifdict[39]="44"
	gifdict[40]="01"
	gifdict[41]="00"
	gifdict[42]="fe"
	gifdict[43]="10"
	gifdict[44]="30"
	gifdict[45]="31"
	gifdict[46]="32"
	gifdict[47]="33"
	gifdict[48]="34"
	gifdict[49]="35"
	gifdict[50]="36"
	gifdict[51]="37"
	gifdict[52]="38"
	gifdict[53]="39"
	gifdict[54]="61"
	gifdict[55]="62"
	gifdict[56]="63"
	gifdict[57]="64"
	gifdict[58]="65"
	gifdict[59]="00"
	gifdict[60]="3b"
	if n>61:
		n-=45
		with open(filename,"w") as fgif:
			for i in range(0,43):
				fgif.write(chr(int(gifdict[i],16)))
			for i in range(n/16):
				for j in range(0,16):
					fgif.write(chr(int(gifdict[43+j],16)))
			k=n % 16
			if k>0:
				fgif.write(chr(k))
				for j in range(0,k-1):
					fgif.write(chr(int(gifdict[44+j],16)))						
			
			for i in range(59,61):
				fgif.write(chr(int(gifdict[i],16)))
	else:
		with open(filename,"w") as fgif:
			fgif.write("A"*n)

#packages
import subprocess
import json
import sys
import os

website=sys.argv[2]
mkdir="mkdir "+website
if not os.path.exists(website):
	subprocess.call(mkdir.split())
data=json.load(open(website+".json"))
init={}
onserver={}
responsesize={}
type={}
root=""
time=""
for i in data:
	if ("initiator" not in i) and (i['type']=='Document')and ((time=="")or(time<i["start_time"])):	
		time=i['start_time']
		root=i['url']
		htmlsize=int(i["response_size"])
		mainaddress=i["remoteIP"]
		rootserver=i["server"]
if root=="":
	print "no file on this server"
	sys.exit()
init[root]="root"
onserver[root]="yes"
responsesize[root]=htmlsize
type[root]='Document'



for i in data:
	if (("initiator" in i) and ("remoteIP" in i)):
		if (i["type"] == "XHR") or (i['url']==root):
			continue
		hostname=i["remoteIP"]
		init[i['url']]=i['initiator']
		responsesize[i['url']]=int(i["response_size"])
		type[i['url']]=i["type"]
		if  (hostname== mainaddress) or (i['server']==rootserver):
			onserver[i['url']]="yes"

		else:
			onserver[i['url']]="no"
		



if sys.argv[1]=="on":
	for i in init:
		if init[i]<>"root":
			current=init[i]
			oncounter=0
			while (current in init) and (oncounter<1000):
				if (onserver[current]=="yes") or (current == init[current]):	
					break
				else:
					current=init[current]
					oncounter+=1
			init[i]=current
	for i in onserver:
		if onserver[i]=="no":
			del init[i]
			del responsesize[i]
			del type[i]


imgcounter=0
scriptcounter=0
sheetcounter=0
fontcounter=0
doccounter=0

mark={}
for i in init:
	if init[i]<>"root":
		if type[i]=="Image":
			mark[i]=imgcounter
			imgcounter+=1
		if type[i]=="Stylesheet":
			mark[i]=sheetcounter
			sheetcounter+=1
		if type[i]=="Font":
			mark[i]=fontcounter
			fontcounter+=1
		if type[i]=="Script":
			mark[i]=scriptcounter
			scriptcounter+=1
		if type[i]=="Document":
			mark[i]=doccounter
			doccounter+=1
for i in init:
	if type[i]=="Image":
		gifg(responsesize[i],website+"/img"+str(mark[i])+".gif")
	if type[i]=="Font":
		with open(website+"/font"+str(mark[i])+".woff","w") as f:
			f.write("A"*(responsesize[i]))
	if type[i]=="Document":
		st="<head>\n"
		st2="-->\n</body>"
		if root==i:
			st3=website+"/index.html"
		else:
			st3=website+"/index"+str(mark[i])+".html"
		with open(st3,"w") as f:
			for j in init:
				if (init[j]==i) and (type[j]=="Stylesheet"):
					st+="<link rel="+'"'+"stylesheet"+'"'
					st+=" href="+'"'+"sheet"+str(mark[j])+".css"+'"'+">\n"
			for j in init:
				if (init[j]==i) and (type[j]=="Document"):
					st+="<iframe src="+'"'
					st+="index"+str(mark[j])+".html"+'"'+"></iframe>\n"
			for j in init:
				if (init[j]==i) and (type[j]=="Script"):
					st+="<script src="+'"'+"script"+str(mark[j])+".js"
					st+='"'+"></script>\n"

			
			st4=""
			for j in init:
				if (init[j]==i) and (type[j]=="Font"):
					st4+="@font-face{\n"
					st4+="font-family:font"+str(mark[j])+";\n"
					st4+="src:url(font"+str(mark[j])+".woff);\n"
					st4+="}\n"
					st4+=".x"+str(mark[j])+"{\n"
					st4+="font-family:font"+str(mark[j])+";\n"
					st4+="}\n"
			if st4<>"":
				st+=("<style>\n"+st4+"</style>\n")

			st+="</head>\n"
			st+="<body>\n"
			for j in init:
				if (init[j]==i) and (type[j]=="Image"):
					st+="<img src="+'"'+"img"+str(mark[j])+".gif"+'"'+">\n"
			for j in init:
				if (init[j]==i) and (type[j]=="Font"):
					st+="<span class="+'"'+"x"+str(mark[j])+'"'+">A</a>\n"
			st+="<!--"
			htmlsize=responsesize[i]-len(st)-len(st2)
			st+=htmlsize*"A"
			st+=st2
			f.write(st)


	if type[i]=="Script":
		front="document.write("+"'"
		back="');"
		st=""
		for j in init:
			if (init[j]==i) and (type[j]=="Stylesheet"):
				st+=front+"<link rel="+'"'+"stylesheet"+'"'
				st+=" href="+'"'+"sheet"+str(mark[j])+".css"+'"'+">"+back
		for j in init:
			if (init[j]==i) and (type[j]=="Script"):
				st+=front+"<script src="+'"'+"script"+str(mark[j])+".js"
				st+='"'+"></script>"+back
		for j in init:
			if (init[j]==i) and (type[j]=="Image"):
				st+=front+"<img src="+'"'+"img"+str(mark[j])+".gif"+'"'+">"+back
		for j in init:
			if (init[j]==i) and (type[j]=="Document"):
				varname="index"+str(mark[j])
				st+="var "+varname+"=document.createElement('iframe');"+varname+".src='"+varname+".html';document.body.appendChild("+varname+");"

		st4=""
		for j in init:
			if (init[j]==i) and (type[j]=="Font"):
				markj=str(mark[j])
				st4+="var t"+markj+"=document.createElement("+'"'+'p'+'"'+");"
				st4+="t"+markj+".innerHTML="+'"'+'H'+'"'+";"
				st4+="var i"+markj+"=new FontFace("+'"'+"I"+markj+'"'+","+'"'+"url(font"+markj+".woff)"+'"'+");"
				st4+="i"+markj+".load().then(function(face){document.fonts.add(face);"
				st4+="t"+markj+".style.fontFamily=face.family;"
				st4+="document.body.appendChild(t"+markj+");});"
				
		if st4<>"":
			st+="window.onload=function(_){"+st4+"};\n"

		with open(website+"/script"+str(mark[i])+".js","w") as f:
			f.write(st+"/*"+"A"*(responsesize[i]-4-len(st))+"*/")
	if type[i]=="Stylesheet":
		with open(website+"/sheet"+str(mark[i])+".css","w") as f:
			f.write("/*"+"A"*(responsesize[i]-4)+"*/")			