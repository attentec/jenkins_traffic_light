from jenkins import Jenkins
import pprint

result_to_color={'SUCCESS': 'G',
                 'UNSTABLE': 'Y',
                 'FAILURE': 'R'}

ServerUrl='http://ci.attentec.se'
JobName = 'Hacka-Traffic-Light'

jenkins = Jenkins(ServerUrl)

jobs = jenkins.get_job_info(JobName, 0, False)
last_completed_job = jobs["lastCompletedBuild"]
last_completed_build_number = last_completed_job["number"]
last_completed_build_info = jenkins.get_build_info(JobName, last_completed_build_number) 
result = last_completed_build_info["result"]

print("{} lastCompletedBuild: {} result: {} color: {}".format(JobName, last_completed_build_number, result, result_to_color[result]))
