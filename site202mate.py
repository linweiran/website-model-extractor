import subprocess
import sys
with open("parsed.txt") as f:
	for lines in f:
		lineup=lines.strip()
		st="python s202.py "+sys.argv[1]+" "+lineup
		print st
		subprocess.call(st.split())

