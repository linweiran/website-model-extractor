import sys
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
n=int(sys.argv[1])
filename=sys.argv[2]
gifg(n,filename)
