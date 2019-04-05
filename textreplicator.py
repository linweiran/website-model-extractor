import sys
origin = sys.argv[1]
dest = sys.argv[2]
times = int(sys.argv[3])
with open(origin, "r") as fr:
	unparsed = fr.readlines()
with open(dest, "w") as fw:
	for i in range(times):
		if i > 0 :
			fw.write("\n")
		for lines in unparsed:
			fw.write(lines)
