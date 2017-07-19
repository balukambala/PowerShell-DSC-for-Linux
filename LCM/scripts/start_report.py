#!/usr/bin/python
"""
This file generates an initial DSC report to indicate that additional reports will be sent.
It requires that a job id and start date are passed in as parameters.
It prints out (returns) a json report that will be sent to the DSC pull service.
"""
import getopt
import sys
import json
import socket

# Process any arguments sent in
job_id = None
start_date = None

opts, args = getopt.getopt(sys.argv[1:], "j:t:")
for o, a in opts:
    if o == '-j':
        job_id = a
    elif o == '-t':
        start_date = a

job_state_json = '''{
	"JobId": "",
	"OperationType": "Consistency",
	"NodeName": "",
	"IpAddress": "",
	"LCMVersion": "2.0",
	"ReportFormatVersion": "2.0",
	"StartTime": "",
	"Errors": [],
	"StatusData": [],
	"AdditionalData": []
}
'''

job_json = json.loads(job_state_json)
job_json['StartTime'] = start_date
job_json['JobId'] = job_id
ipaddress = socket.gethostbyname(socket.getfqdn())
job_json['IpAddress'] = ipaddress
job_json['NodeName'] = socket.getfqdn()
print json.dumps(job_json)
