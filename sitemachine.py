#packages
import subprocess
import json
import sys
import os

#initializtion
img={}
imgcounter=0
script={}
scriptcounter=0
sheet={}
sheetcounter=0
font={}
fontcounter=0

website=sys.argv[1]
mkdir="mkdir "+website
if not os.path.exists(website):
	subprocess.call(mkdir.split())


#read
data=json.load(open(website+".json"))
for i in data:
	size=int(i["response_size"])
	if i["type"]=="Script":
		script[scriptcounter]=size
		scriptcounter+=1
	if i["type"]=="Image":
		img[imgcounter]=size
		imgcounter+=1
	if i["type"]=="Stylesheet":
		sheet[sheetcounter]=size
		sheetcounter+=1
	if i["type"]=="Document":
		htmlsize=size
	if i["type"]=="Font":
		font[fontcounter]=size
		fontcounter+=1
	
st="<head>\n"
st2="-->\n</body>"
with open(website+"/index.html","w") as f:
	for i in sheet:
		st+="<link rel="+'"'+"stylesheet"+'"'
		st+=" href="+'"'+"sheet"+str(i)+".css"+'"'+">\n"
	for i in script:
		st+="<script src="+'"'+"script"+str(i)+".js"
		st+='"'+"></script>\n"

	if fontcounter>0:
		st+="<style>\n"
		st+="@font-face{\n"
		st+="font-family:font1;\n"
		for i in font:
			st+="src:url(font"+str(i)+".woff);\n"
		st+="}\n"
		st+="*{\n"
		st+="font-family:font1;\n"
		st+="}\n"
		st+="</style>\n"



	st+="</head>\n"
	st+="<body>\n"
	for i in img:
		st+="<img src="+'"'+"img"+str(i)+".png"+'"'+">\n"
	st+="<!--"
	htmlsize=htmlsize-len(st)-len(st2)
	st+=htmlsize*"A"
	st+=st2
	f.write(st)
	
	

for i in img:
	with open(website+"/img"+str(i)+".png","w") as f:
		f.write("A"*img[i])

for i in script:
	with open(website+"/script"+str(i)+".js","w") as f:
		f.write("/*"+"A"*(script[i]-4)+"*/")

for i in sheet:
	with open(website+"/sheet"+str(i)+".css","w") as f:
		f.write("/*"+"A"*(sheet[i]-4)+"*/")
for i in font:
	with open(website+"/font"+str(i)+".woff","w") as f:
		f.write("A"*font[i])
	