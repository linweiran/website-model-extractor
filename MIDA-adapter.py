import os
import subprocess
import json
import sys

writeto='http-origin'
mkdir="mkdir "+writeto
if not os.path.exists(writeto):
	subprocess.call(mkdir.split())
inputfile=open("parsed.txt","r")
sites = inputfile.readlines()
for website in sites:
	website=website.strip()
	step = 0
	path = './results/'+website+"/"
	dir_list = [directory for directory in os.listdir(path) if os.path.isdir(path+directory)]
	for hashes in dir_list:
		print website+" "+hashes+" "+str(step)
		data=json.load(open(path+hashes+"/resource_metadata.json"))
		
		requests = {}
		for requestId in data:
			connection = data[requestId]
			request = connection["requests"][0]
			response = connection["responses"][0]
			if response["response"]["headers"] is None:
				continue
			if "content-length" not in response["response"]["headers"]:
				continue
			requests[requestId]={}
			#requests[requestId]['request_size'] = missing ? request headers?
			requests[requestId]['start_time'] = request["timestamp"]
			requests[requestId]['server'] = "not used"
			requests[requestId]['type'] = request["type"]
			requests[requestId]['response_size'] = response["response"]["headers"]["content-length"]	
			initiator = request["initiator"]
			if "url" in initiator:			
				requests[requestId]['initiator'] = initiator["url"]
			requests[requestId]['connection']=response["response"]['connectionId']
			requests[requestId]['remoteIP'] =response["response"]['remoteIPAddress']
			requests[requestId]['end_time'] = response["timestamp"]
			with open("http-origin/"+website+"-"+str(step+1)+".json","w") as f:
				json_out = []
				for rid, request in requests.items():
					if 'connection' in request:
						json_out.append(request)
				json.dump(json_out, f)
		step = step +1
