def ireport(n,m,s):
	if n>1:
		print str(n)+" "+s+"s of size "+str(m)
	else:
		print str(n)+" "+s+" of size "+str(m) 



import json
import sys

criterion=sys.argv[1]
target=sys.argv[2]
cdata=json.load(open(criterion))
tdata=json.load(open(target))

cdict={}
for i in cdata:
	size=int(i["response_size"])
	type=i["type"]
	if type not in cdict:
		cdict[type]={}
	if size not in cdict[type]:
		cdict[type][size]=1
	else:
		cdict[type][size]+=1

tdict={}
for i in tdata:
	size=int(i["response_size"])
	type=i["type"]
	if type not in tdict:
		tdict[type]={}
	if size not in tdict[type]:
		tdict[type][size]=1
	else:
		tdict[type][size]+=1

print "missing:"
for i in cdict:
	if i not in tdict:
		for j in cdict[i]:
			ireport(cdict[i][j],j,i)
	else:
		for j in cdict[i]:
			if j not in tdict[i]:
				ireport(cdict[i][j],j,i)
			else:
				if cdict[i][j]>tdict[i][j]:
					ireport(cdict[i][j]-tdict[i][j],j,i)

print "extra:"
for i in tdict:
	if i not in cdict:
		for j in tdict[i]:
			ireport(tdict[i][j],j,i)
	else:
		for j in tdict[i]:
			if j not in cdict[i]:
				ireport(tdict[i][j],j,i)
			else:
				if tdict[i][j]>cdict[i][j]:
					ireport(tdict[i][j]-cdict[i][j],j,i)




