import os
import sys
path=sys.argv[1]
dict={}
with open("size.csv","w") as s:
	for o in os.listdir(path):
		if os.path.isdir(o) and o!=".git":
			size = 0
			for f in os.listdir(o):
				size +=os.path.getsize(o+"/"+f)
			filename=o.split("_")[0]
			number=o.split("_")[1]
			if filename not in dict:
				dict[filename]={}
			dict[filename][number]=str(size)
	for filename in dict:
		for number in dict[filename]:
			s.write("{},{},{}\n".format(filename,number,dict[filename][number]))
			