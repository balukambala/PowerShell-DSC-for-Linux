#!/usr/bin/python
import getopt
import sys
import os
import json
import socket

# Process any arguments sent in
job_id = None
configuration_mode = None
error_message = None
source_info = None
module_name = None
number_of_resources = None
duration = None
instance_name = None
start_date = None
end_date = None
resource_name = None
existing_list = None
module_version = None
reboot_requested = None
reboot_node_needed = None
resource_id = None
configuration_name = None
in_desired_state = None

opts, args = getopt.getopt(sys.argv[1:], "j:a:p:h:e:s:m:d:i:t:l:n:v:b:f:r:c:k:")
for o, a in opts:
    if o == '-j':
        job_id = a
    if o == '-a':
        configuration_mode = a
    if o == '-h':
        number_of_resources = a
    if o == '-p':
        error_message = a
    if o == '-e':
        existing_list = a
    if o == '-s':
        source_info = a
    elif o == '-m':
        module_name = a
    elif o == '-d':
        duration = a
    elif o == '-i':
        instance_name = a
    elif o == '-l':
        start_date = a
    elif o == '-t': 
        end_date = a
    elif o == '-n': 
        resource_name = a
    elif o == '-v': 
        module_version = a
    elif o == '-b': 
        reboot_requested = a
    elif o == '-f': 
        reboot_node_needed = a
    elif o == '-r': 
        resource_id = a
    elif o == '-c': 
        configuration_name = a
    elif o == '-k': 
        in_desired_state = a

job_state_json = ''' 
{
	"JobId": "",
	"OperationType": "Consistency",
	"RefreshMode": "Pull",
	"Status": "Success",
	"ReportFormatVersion": "2.0",
	"ConfigurationVersion": "2.0.0",
	"StartTime": "",
	"RebootRequested": "False",
	"Errors": [],
	"StatusData": [],
	"AdditionalData":[]
}
'''

desired_state_json = '''{
"StartDate" : "",
"IPV6Addresses" : [],
"DurationInSeconds" : "",
"JobID" : "",
"CurrentChecksum" : "",
"MetaData" : "",
"Status" : "Success",
"IPV4Addresses" : [],
"LCMVersion" : "2.0",
"ResourcesInDesiredState"  : [],
"ResourcesNotInDesiredState" : [],
"NumberOfResources" : "",
"Type" : "Consistency",
"HostName" : "",
"RebootRequested" : "",
"MACAddresses" : [""],
"MetaConfiguration" : {
	"AgentId": "",
	"SignatureValidations": [],
	"ConfigurationDownloadManagers": [{
		"RegistrationKey": "",
		"ServerURL": "",
		"ResourceId": "[","ConfigurationNames": [""],
		"SourceInfo": ""
        }],
	"ActionAfterReboot": "ContinueConfiguration",
	"LCMCompatibleVersions": ["1.0", "2.0"],
	"LCMState": "Idle",
	"ResourceModuleManagers": [{
		"RegistrationKey": "",
		"ServerURL": "",
		"ResourceId": "[ResourceRepositoryWeb]AzureAutomationDSC",
		"SourceInfo": ""
	}],
	"ReportManagers": [{
		"RegistrationKey": "",
		"ServerURL": "",
		"ResourceId": "[ReportServerWeb]AzureAutomationDSC",
		"SourceInfo": ""
	}],
	"StatusRetentionTimeInDays": "",
	"LCMVersion": "2.0",
	"MaximumDownloadSizeMB": "",
	"ConfigurationMode": "",
	"RefreshFrequencyMins": "",
	"RebootNodeIfNeeded": "",
	"SignatureValidationPolicy": "NONE",
	"RefreshMode": "Pull",
	"DebugMode": ["NONE"],
	"CertificateID": "",
	"AllowModuleOverwrite": "",
	"ConfigurationModeFrequencyMins": "",
	"LCMStateDetail": ""
},
"Locale" : "en-US",
"Mode" : ""
}
'''

error_state_json = '''
{
   "ErrorSource":"DSCPowershellResource",
   "Locale":"en-US",
   "Errors":"{}",
   "ErrorCode":"1",
   "ErrorMessage":"",
   "ResourceId":"[Package]OMS"
}
'''

json_value = json.loads(desired_state_json)

with open(existing_list) as json_file:
    json_state = json.load(json_file)

json_value['JobID'] = job_id
json_value['Mode'] = "Pull"
json_value['MetaConfiguration']['ConfigurationMode'] = configuration_mode
json_value['MetaConfiguration']['RebootNodeIfNeeded'] = reboot_node_needed
json_value['StartDate'] = start_date
json_value['NumberOfResources'] = number_of_resources
json_value['ResourcesInDesiredState'] = json_state['ResourcesInDesiredState']
json_value['ResourcesNotInDesiredState'] = json_state['ResourcesNotInDesiredState']
json_value['HostName'] = socket.getfqdn()
ipaddress = socket.gethostbyname(socket.getfqdn())
json_value['IPV4Addresses'].append(ipaddress)
json_value['IPV6Addresses'].append(ipaddress)

job_json = json.loads(job_state_json)
job_json['StartTime'] = start_date
job_json['JobId'] = job_id

# If an error message was passed in, add it to the resource state
if error_message is not None:
    json_value['Error'] = error_message
    json_value['Status'] = "Failure"
    job_json['Status'] = "Failure"
    json_error = json.loads(error_state_json)
    failedResources = json_state['ResourcesNotInDesiredState']
    for error in failedResources:
        json_error['Errors'] = json.loads(error['Error'])
        json_error['ResourceId'] = error['ResourceId']
        json_error['ErrorMessage'] = json_error['Errors']['Exception']['Message']
        job_json['Errors'].append(json.dumps(json_error))
 

# else only send StatusData and EndTime if it is not an error
else:
    job_json['StatusData'].append(json.dumps(json_value))
    job_json['EndTime'] = end_date

if existing_list:
    os.remove(existing_list)

print json.dumps(job_json)
