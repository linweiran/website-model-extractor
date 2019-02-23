#packages
import subprocess
import json
import sys
import os
import random
import hpack

HUFFMAN_PATH = "chars.txt"

# dictionary of Huffman padded extensions
EXT_PADS = {
    'gif':  'aaz.gif',
    'html': 'ab.html',
    'woff': 'aa.woff',
    'js':   'aabb.js',
    'css':  'bbz.css'
}

# list of 7-bit huffman characters
HUFFMAN_CHARS = []
with open(HUFFMAN_PATH) as f:
    for line in f:
        HUFFMAN_CHARS.append(line.split('\n')[0])

# dictionary of used filenames for each site
USED_NAMES = {}

def gen_filename(type, sitecounter):
    filename = ''
    # generate unique 3-char name
    while True:
        filename = ''
        for i in range(3):
            filename += random.choice(HUFFMAN_CHARS)

        if filename not in USED_NAMES[sitecounter]:
            USED_NAMES[sitecounter].add(filename)
            break

    # append extension
    filename += EXT_PADS[type]
    return filename

def sixdigit(n):
	strn=str(n)
	lenn=len(strn)
	if lenn<6 :
		strn= (6-lenn)*"0"+strn
	return strn

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





def sitegenerate(website,sitecounter,instancecounter,padding):
	USED_NAMES[sitecounter] = set()
	writeto="s"+sixdigit(sitecounter)+"_"+sixdigit(instancecounter)
	mkdir="mkdir "+writeto
	if not os.path.exists(writeto):
		subprocess.call(mkdir.split())
	data=json.load(open(website+"-"+str(1+instancecounter)+".json"))
	init={}
	onserver={}
	responsesize={}
	type={}
	filenamepad={}
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
		return
	init[root]="root"
	onserver[root]="yes"
	responsesize[root]=htmlsize
	type[root]='Document'
	filenamepad[root]="index.html"



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
				filenamepad[i]=gen_filename("gif",sitecounter)
			if type[i]=="Stylesheet":
				mark[i]=sheetcounter
				sheetcounter+=1
				filenamepad[i]=gen_filename("css",sitecounter)
			if type[i]=="Font":
				mark[i]=fontcounter
				fontcounter+=1
				filenamepad[i]=gen_filename("woff",sitecounter)
			if type[i]=="Script":
				mark[i]=scriptcounter
				scriptcounter+=1
				filenamepad[i]=gen_filename("js",sitecounter)
			if type[i]=="Document":
				mark[i]=doccounter
				doccounter+=1
				filenamepad[i]=gen_filename("html",sitecounter)
	for i in init:
		if type[i]=="Image":
			gifg(responsesize[i],writeto+"/"+filenamepad[i])
		if type[i]=="Font":
			with open(writeto+"/"+filenamepad[i],"w") as f:
				f.write("A"*(responsesize[i]))
		if type[i]=="Document":
			st="<head>\n"
			st2="-->\n</body>"
			if root==i:
				st3=writeto+"/index.html"
			else:
				st3=writeto+"/"+filenamepad[i]
			with open(st3,"w") as f:
				for j in init:
					if (init[j]==i) and (type[j]=="Stylesheet"):
						st+="<link rel="+'"'+"stylesheet"+'"'
						st+=" href="+'"'+filenamepad[j]+'"'+">\n"
				for j in init:
					if (init[j]==i) and (type[j]=="Document"):
						st+="<iframe src="+'"'
						st+=filenamepad[j]+'"'+"></iframe>\n"
				for j in init:
					if (init[j]==i) and (type[j]=="Script"):
						st+="<script src="+'"'+filenamepad[j]
						st+='"'+"></script>\n"
	
			
				st4=""
				for j in init:
					if (init[j]==i) and (type[j]=="Font"):
						st4+="@font-face{\n"
						st4+="font-family:font"+str(mark[j])+";\n"
						st4+="src:url("+filenamepad[j]+");\n"
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
						st+="<img src="+'"'+filenamepad[j]+'"'+">\n"
				for j in init:
					if (init[j]==i) and (type[j]=="Font"):
						st+="<span class="+'"'+"x"+str(mark[j])+'"'+">A</a>\n"

				if root==i :
					st+= '<script src="'+padding+'"></script>\n'
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
					st+=" href="+'"'+filenamepad[j]+'"'+">"+back
			for j in init:
				if (init[j]==i) and (type[j]=="Script"):
					st+=front+"<script src="+'"'+filenamepad[j]
					st+='"'+"></script>"+back
			for j in init:
				if (init[j]==i) and (type[j]=="Image"):
					st+=front+"<img src="+'"'+filenamepad[j]+'"'+">"+back
			for j in init:
				if (init[j]==i) and (type[j]=="Document"):
					varname="index"+str(mark[j])
					st+="var "+varname+"=document.createElement('iframe');"+varname+".src='"+filenamepad[j]+"';document.body.appendChild("+varname+");"

			st4=""
			for j in init:
				if (init[j]==i) and (type[j]=="Font"):
					markj=str(mark[j])
					st4+="var t"+markj+"=document.createElement("+'"'+'p'+'"'+");"
					st4+="t"+markj+".innerHTML="+'"'+'H'+'"'+";"
					st4+="var i"+markj+"=new FontFace("+'"'+"I"+markj+'"'+","+'"'+"url("+filenamepad[j]+")"+'"'+");"
					st4+="i"+markj+".load().then(function(face){document.fonts.add(face);"
					st4+="t"+markj+".style.fontFamily=face.family;"
					st4+="document.body.appendChild(t"+markj+");});"
					
			if st4<>"":
				st+="window.onload=function(_){"+st4+"};\n"
	
			with open(writeto+"/"+filenamepad[i],"w") as f:
				f.write(st+"/*"+"A"*(responsesize[i]-4-len(st))+"*/")
		if type[i]=="Stylesheet":
			with open(writeto+"/"+filenamepad[i],"w") as f:
				f.write("/*"+"A"*(responsesize[i]-4)+"*/")	




inputfile=open("parsed.txt","r")
unparsedsites= inputfile.readlines()
sitecounter=0
instancenumber=int(sys.argv[1])
with open("size.csv") as f:
	text=f.readlines()
paddingsize={}
for lines in text:
	line=lines.strip().split(",")
	name=line[0]+"_"+line[1]
	value=int(line[2])
	paddingsize[name]=random.randint(4,int(value/4))
for site in unparsedsites:
	website=site.strip()
	for j in range(instancenumber):
		padding=gen_filename("js",sitecounter)
		sitegenerate(website,sitecounter,j,padding)
		writeto="s"+sixdigit(sitecounter)+"_"+sixdigit(j)
		with open(writeto+"/"+padding,"w") as f:
			f.write("/*"+"A"*(paddingsize[writeto]-4)+"*/")
	print website
	sitecounter +=1

	