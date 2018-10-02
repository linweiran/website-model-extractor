import subprocess
import sys
website=sys.argv[1]
instances=int(sys.argv[2])
mode=sys.argv[3]
for i in range(1,instances+1):
	instancename=website+"-"+str(i)
	with open("parsed.txt","a") as f:
		f.write("{}\n".format(instancename))
		cpjson="cp "+instancename+".json "+website+".json"
		mvdir="mv "+website+" "+instancename
		st="python s202.py "+mode+" "+website
		print st
		step1=subprocess.Popen(cpjson.split())
		step1.wait()
		step2=subprocess.Popen(st.split())
		step2.wait()
		step3=subprocess.Popen(mvdir.split())
		step3.wait()
