from jenkins import Jenkins
import pprint

result_to_color={'SUCCESS': 'G',
                 'UNSTABLE': 'Y',
                 'FAILURE': 'R',
                 'BUILDING': 'B'}

SERVER_URL='http://ci.attentec.se'
JOB_NAME = 'Hacka-Traffic-Light'

jenkins = Jenkins(SERVER_URL)

jobs = jenkins.get_job_info(JOB_NAME, 0, False)
last_build = jobs["lastBuild"]
last_build_number = last_build["number"]

NrOfStatuses = min(10, last_build_number)
results= [None] * NrOfStatuses

for i in range(len(results)):
    build_info = jenkins.get_build_info(JOB_NAME, last_build_number-i)
    if build_info["result"] is None:
        results[i] = 'BUILDING'    
    else:
        results[i] = build_info["result"]
    print("build: {} result: {}".format(last_build_number-i, result_to_color[results[i]]))
