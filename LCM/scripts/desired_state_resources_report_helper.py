#!/usr/bin/python
"""
This file generates a json file that stores information about a resource.
If an existing json file path is passed in, it will append to this json object.
It saves the json file to a tmp file and returns the path to the caller.
"""
import getopt
import sys
import os
import json
import tempfile

# Process any arguments sent in
source_info = None
module_name = None
duration = None
instance_name = None
start_date = None
resource_name = None
existing_list = None
module_version = None
reboot_requested = None
resource_id = None
configuration_name = None
in_desired_state = None
error_string = ""

opts, args = getopt.getopt(sys.argv[1:], "e:s:m:d:i:t:n:a:v:b:r:c:k:")
for o, a in opts:
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
    elif o == '-t':
        start_date = a
    elif o == '-n':
        resource_name = a
    elif o == '-a':
        error_string = a
    elif o == '-v':
        module_version = a
    elif o == '-b':
        reboot_requested = a
    elif o == '-r':
        resource_id = a
    elif o == '-c':
        configuration_name = a
    elif o == '-k':
        in_desired_state = a

error_json = '''{
   "Exception":{
      "Message":"",
      "Data":{
      },
      "InnerException":{
         "ErrorRecord":"",
         "WasThrownFromThrowStatement":"",
         "Message":"",
         "Data":"",
         "InnerException":"",
         "TargetSite":"",
         "StackTrace":"",
         "HelpLink":"",
         "Source":"",
         "HResult":""
      },
      "TargetSite":"",
      "StackTrace":"",
      "HelpLink":"",
      "Source":"",
      "HResult":""
   },
   "TargetObject":"",
   "CategoryInfo":{
      "Category":"",
      "Activity":"",
      "Reason":"",
      "TargetName":"",
      "TargetType":""
   },
   "FullyQualifiedErrorId":"",
   "ErrorDetails":"",
   "InvocationInfo":"",
   "ScriptStackTrace":"",
   "PipelineIterationInfo":[]
}
'''

state_json = '''{
"ResourcesInDesiredState"  : [],
"ResourcesNotInDesiredState" : []
	}
'''

resource_state = ''' {
	"SourceInfo": "",
	"ModuleName": "",
	"DurationInSeconds": "",
	"InstanceName": "",
	"StartDate": "",
	"ResourceName": "",
	"ModuleVersion": "",
	"RebootRequested": "",
	"ResourceId": "",
	"ConfigurationName": "",
	"InDesiredState": ""
}
'''

if existing_list is None:
    json_state = json.loads(state_json)
else:
    with open(existing_list) as json_file:
        json_state = json.load(json_file)

# Set the values on the resource from the passed in arguments
json_resource_state = json.loads(resource_state)
json_resource_state['SourceInfo'] = source_info
json_resource_state['ModuleName'] = module_name
json_resource_state['DurationInSeconds'] = duration
json_resource_state['InstanceName'] = instance_name
json_resource_state['StartDate'] = start_date
json_resource_state['ResourceName'] = resource_name
json_resource_state['ModuleVersion'] = module_version
json_resource_state['RebootRequested'] = reboot_requested
json_resource_state['ResourceId'] = resource_id
json_resource_state['ConfigurationName'] = configuration_name
json_resource_state['InDesiredState'] = in_desired_state

if len(error_string) > 1:
    json_error_state = json.loads(error_json)
    json_error_state['Exception']['Message'] = error_string
    json_error_state['Exception']['InnerException']['Message'] = error_string
    json_resource_state['Error'] = json.dumps(json_error_state)

# If the resource is not in a desired state, set to False, otherwise set to True
if in_desired_state == "False":
    json_state['ResourcesNotInDesiredState'].insert(0, json_resource_state)
else:
    json_state['ResourcesInDesiredState'].insert(0, json_resource_state)

# Create temporary file to store json and return the path to the caller
temp = tempfile.NamedTemporaryFile(delete=False)
temp.write(json.dumps(json_state))
temp.close()
if existing_list:
    os.remove(existing_list)

sys.stdout.write(temp.name)
sys.stdout.flush()
