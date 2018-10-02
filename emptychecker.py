import sys
datamode=sys.argv[1]
sites=int(sys.argv[2])
num=int(sys.argv[3])
for i in range(sites):
	for j in range(num):
		if datamode=="knn":
			filename=str(i)+"-"+str(j)
		if datamode=="kfp":
			filename=str(i)+"_"+str(j)
		with open(filename) as f:
			counter=0
			for lines in f:
				counter+=1
			if counter==0:
				print filename