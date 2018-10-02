def cut(s,n):
    return s


def check(id,answer,fs,length):
    if (id in answer):
        fs.write("{}".format(cut(str(answer[id]),length)))
    else:
        fs.write("{}".format(cut("***",length)))


import pychrome
from subprocess import Popen, DEVNULL
import subprocess
import shutil
from pathlib import Path
import argparse
import time
import sys
import socket
import traceback
import random
import json
from urllib.parse import urlparse, urlunparse

parser = argparse.ArgumentParser()
parser.add_argument("-P", "--chrome-path", action='store')
args = parser.parse_args()

print(args)
if not args.chrome_path:
    if shutil.which("chromium-browser"):
        args.chrome_path = "chromium-browser"
    else:
        osx_canary = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        if Path(osx_canary).is_file():
            args.chrome_path = osx_canary
        else:
            print("Cannot find chrome")
            sys.exit(1)


http = Path('http')
if not http.is_dir():
    http.mkdir()
inputfile=open("parsed.txt","r")
sites = inputfile.readlines()
random.shuffle(sites)

for website in sites:
    website=website.strip()
    if Path('http/' + website + '.json').exists():
        continue

    print("Loading", website)
    with Popen([args.chrome_path, "--remote-debugging-port=9222", "--headless", "--disable-gpu"], stdout=DEVNULL, stderr=DEVNULL) as chrome:
        time.sleep(5)

        print("Loading...")

        # create a browser instance
        browser = pychrome.Browser(url="http://127.0.0.1:9222")

        # create a tab
        tab = browser.new_tab()

        urls = {}
        requests = {}
        answerserver={}
        answerreqeustsize={}
        answerresponsesize={}
        answerinitiator={}
        answerconnection={}
        # register callback if you want
        def request_will_be_sent(*, request, requestId, timestamp, type=None, **kwargs):
            requests[requestId] = {}
            requests[requestId]['url'] = request['url']
            parsed_url = urlparse(request['url'])
            size = len(request['method']) + len(' ') + len(' HTTP/1.1\r\n\r\n')
            size += len(urlunparse(['',''] + list(parsed_url[2:])))
            for k,v in request['headers'].items():
                size += len(k) + len(v) + 4 # colon, space, \r\n
            if "postData" in request:
                size += len(request['postData'])
            requests[requestId]['request_size'] = size
            requests[requestId]['start_time'] = timestamp
            requests[requestId]['server'] = parsed_url.netloc
            requests[requestId]['type'] = type
            requests[requestId]['response_size']=0
        #		print("Loading", request['url'], requests[requestId])
            if kwargs['initiator']['type'] in {'parser','script'}:
                if 'url' in kwargs['initiator']:
                    requests[requestId]['initiator']=kwargs['initiator']['url']
                else:
                    if 'stack' in kwargs['initiator']:
                        requests[requestId]['initiator']=kwargs['initiator']['stack']['callFrames'][0]['url']
                    

        def response_received(*, requestId, response, **kwargs):
            requests[requestId]['connection'] = response['connectionId']

        def loading_finished(*, requestId, encodedDataLength, timestamp, **kwargs):
            if requestId in requests:
                requests[requestId]['end_time'] = timestamp
 
        def data_received(*,requestId,timestamp,dataLength,encodedDataLength, **kwargs):
                 print ("$$$$url",requests[requestId]['url'],"$$$dataLength",dataLength,"$$$encodedDataLength",encodedDataLength)
                 requests[requestId]['response_size']+=dataLength


        #print("Finished loading", requests[requestId]['url'], requests[requestId])

        tab.Network.requestWillBeSent = request_will_be_sent
        tab.Network.loadingFinished = loading_finished
        tab.Network.responseReceived = response_received
        tab.Network.dataReceived=data_received


        # start the tab
        tab.start()

        # call method
        tab.Network.enable()
        # call method with timeout
        tab.Page.navigate(url="https://"+website+"/", _timeout=5)

        # wait for loading
        tab.wait(5)

        # stop the tab (stop handle events and stop recv message from chrome)
        tab.stop()

        # close tab
        browser.close_tab(tab)

        connections = set()
        sent_size = 0
        leaf_size = 0
        non_leaf_size = 0
        num_requests = 0
        with open("http/"+website+".json","w") as f:
        #f.write("{},{},{},{},{},{},{}\n".format(cut("requestid",10),cut("url",45),cut("server",30),cut("reqsize",7),cut("ressize",7),cut("initiator",45),"connectionID"))
            json_out = []
            for rid, request in requests.items():
                if request['server'] == website:
                    json_out.append(request)
                    connections.add(request['connection'])
                    sent_size += request['request_size']
                    print("##", request['type'], request['response_size'])
                    if request['type'] in ['Image']:
                        leaf_size += request['response_size']
                    else:
                        non_leaf_size += request['response_size']
                    num_requests += 1
            json.dump(json_out, f)
        print("{}: {} requests over {} connections, {} up, {} non-leaf down, {} leaf down".format(website,
            num_requests, len(connections), sent_size, non_leaf_size, leaf_size))
        chrome.terminate()
