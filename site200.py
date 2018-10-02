#packages
import subprocess
import json
import sys
import os


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











website=sys.argv[1]
mkdir="mkdir "+website
if not os.path.exists(website):
	subprocess.call(mkdir.split())



imgstart=0
imgend=0

scriptstart=0
scriptend=0

sheetstart=0
sheetend=0

fontstart=0
fontend=0

docstart=0
docend=0


#read
data=json.load(open(website+".json"))
dict={}
for i in data:
	if ("initiator" not in i) and (i['type']=='Document'):
		dict[0]=i
pointer=0
mark={}
taker=0
while(taker<=pointer):
	i=dict[taker]
	taker+=1
	url=i['url']
	if i['type']=='Document':
		for j in data:
			if "initiator" in j:
				if j["initiator"]==url:
					if j["type"]=="Image":
							gifg(int(j["response_size"]),website+"/img"+str(imgend)+".gif")
							imgend +=1
					if j["type"]=="Stylesheet":
							pointer+=1
							dict[pointer]=j
							mark[pointer]=sheetend
							sheetend+=1
					if j["type"]=="Font":
							with open(website+"/font"+str(fontend)+".woff","w") as f:
								f.write("A"*(int(j["response_size"])))
							fontend+=1
					if j["type"]=="Script":
							pointer+=1
							dict[pointer]=j
							mark[pointer]=scriptend
							scriptend+=1
					if j["type"]=="Document":
							pointer+=1
							dict[pointer]=j
							mark[pointer]=docend
							docend+=1
		st="<head>\n"
		st2="-->\n</body>"
		if taker==1:
			st3=website+"/index.html"
		else:
			st3=website+"/index"+str(mark[taker-1])+".html"
		with open(st3,"w") as f:
			for t in range(sheetstart,sheetend):
				st+="<link rel="+'"'+"stylesheet"+'"'
				st+=" href="+'"'+"sheet"+str(t)+".css"+'"'+">\n"
			sheetstart=sheetend
			for t in range(docstart,docend):
				st+="<link rel="+'"'+"import"+'"'
				st+=" href="+'"'+"index"+str(t)+".html"+'"'+">\n"
			docstart=docend
			for t in range(scriptstart,scriptend):
				st+="<script src="+'"'+"script"+str(t)+".js"
				st+='"'+"></script>\n"
			scriptstart=scriptend
			if fontend>fontstart:
				st+="<style>\n"
				st+="@font-face{\n"
				st+="font-family:font1;\n"
				for t in range(fontstart,fontend):
					st+="src:url(font"+str(t)+".woff);\n"
				st+="}\n"
				st+="*{\n"
				st+="font-family:font1;\n"
				st+="}\n"
				st+="</style>\n"
				fontstart=fontend
			st+="</head>\n"
			st+="<body>\n"
			for t in range(imgstart,imgend):
				st+="<img src="+'"'+"img"+str(t)+".gif"+'"'+">\n"
			st+="<!--"
			imgstart=imgend
			htmlsize=int(i["response_size"])-len(st)-len(st2)
			st+=htmlsize*"A"
			st+=st2
			f.write(st)					
					

	if i['type']=='Script':
		for j in data:
			if "initiator" in j:
				if j["initiator"]==url:
					if j["type"]=="Image":
							gifg(int(j["response_size"]),website+"/img"+str(imgend)+".gif")
							imgend+=1
					if j["type"]=="Stylesheet":
							pointer+=1
							dict[pointer]=j
							mark[pointer]=sheetend
							sheetend+=1							
					if j["type"]=="Font":
							with open(website+"/font"+str(fontend)+".woff","w") as f:
								f.write("A"*(int(j["response_size"])))
							fontend+=1
					if j["type"]=="Script":
							pointer+=1
							dict[pointer]=j
							mark[pointer]=scriptend
							scriptend+=1
					if j["type"]=="Document":
							pointer+=1
							dict[pointer]=j
							mark[pointer]=docend
							docend+=1
		front="document.write("+"'"
		back="');"
		st=""
		for t in range(sheetstart,sheetend):
			st+=front+"<link rel="+'"'+"stylesheet"+'"'
			st+=" href="+'"'+"sheet"+str(t)+".css"+'"'+">"+back
		sheetstart=sheetend
		for t in range(scriptstart,scriptend):
			st+=front+"<script src="+'"'+"script"+str(t)+".js"
			st+='"'+"></script>"+back
		scriptstart=scriptend
		for t in range(imgstart,imgend):
			st+=front+"<img src="+'"'+"img"+str(t)+".gif"+'"'+">"+back
		imgstart=imgend
		for t in range(docstart,docend):
			st+=front+"<iframe src="+'"'+"index"+str(t)+".html"+'"'+"></iframe>"+back
		docstart=docend

		with open(website+"/script"+str(mark[taker-1])+".js","w") as f:
			f.write(st+"/*"+"A"*(int(i["response_size"])-4-len(st))+"*/")

	if i['type']=='Stylesheet':
		for j in data:
			if "initiator" in j:
				if j["initiator"]==url:
					if j["type"]=="Stylesheet":
							pointer+=1
							dict[pointer]=j
							mark[pointer]=sheetend
							sheetend+=1							
					if j["type"]=="Font":
							with open(website+"/font"+str(fontend)+".woff","w") as f:
								f.write("A"*(int(j["response_size"])))
							fontend+=1
		st=""
		for t in range(sheetstart,sheetend):
			st+="@import "+'"'+"sheet"+str(t)+".css"+'"'+";\n"
		sheetstart=sheetend		
		if fontend>fontstart:
			st+="@font-face{\n"
			st+="font-family:font1;\n"
			for t in range(fontstart,fontend):
				st+="src:url(font"+str(t)+".woff);\n"
			st+="}\n"
			st+="*{\n"
			st+="font-family:font1;\n"
			st+="}\n"
			st+="</style>\n"
			fontstart=fontend		
		
		with open(website+"/sheet"+str(mark[taker-1])+".css","w") as f:
			f.write(st+"/*"+"A"*(int(i["response_size"])-4-len(st))+"*/")



#css to css: @import "name.css"
#css to font: 
#@font-face{
#font-family: 'Myfont';
#src: url('font1.woff') format('woff');
#     url('font1.woff') format('woff');
#}