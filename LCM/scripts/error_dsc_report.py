#!/usr/bin/python
"""
This file generates an error DSC report to indicate that an error has occurent. Aadditional reports will be sent.
It requires that a job id and start date are passed in as parameters.
It prints out (returns) a json report that will be sent to the DSC pull service.
"""

import getopt
import sys
import os
import json
import datetime

# Process any arguments sent in
job_id, start_date = None, None
opts, args = getopt.getopt(sys.argv[1:], "j:t:")
for o, a in opts:
    if o == '-j': 
        job_id = a
    elif o == '-t': 
        start_date = a

json_error = '''{
    "JobId": "",
    "OperationType": "Consistency",
    "Status": "Failure",
    "ReportFormatVersion": "2.0",
    "StartTime": "",
    "Errors": [],
    "StatusData": [],
    "AdditionalData": []
    }
'''

error_message = '''{
	"Locale": "en-US",
	"ErrorCode": "1",
	"ErrorMessage": "The SendConfigurationApply function did not succeed.",
	"ResourceId": "DSCEngine",
	"ErrorSource": "DSCEngine"
}
'''

json_error_state = json.loads(json_error)
json_error_message = json.loads(error_message)
json_error_state['StartTime'] = start_date
json_error_state['JobId'] = job_id
json_error_state['Errors'].append(json.dumps(json_error_message))
print json.dumps(json_error_state)

