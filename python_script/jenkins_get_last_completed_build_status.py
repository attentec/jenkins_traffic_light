from jenkins import Jenkins
import pprint
import os
from time import sleep

result_to_color={'SUCCESS': 'G',
                 'UNSTABLE': 'Y',
                 'FAILURE': 'R'}

SERVER_URL='http://ci.attentec.se'
JOB_NAME = 'Hacka-Traffic-Light'



def get_jenkins_build_info(jenkins, job_name, build_type):
	jobs = jenkins.get_job_info(job_name, 0, False)
	job = jobs[build_type]
	build_number = job["number"]
	build_info = jenkins.get_build_info(JOB_NAME, build_number) 
	return build_info

def main():
	prev_res = ""

	while True:		
		build_info = get_jenkins_build_info(jenkins, JOB_NAME, "lastCompletedBuild")
		result = build_info["result"]
		if result_to_color[result] != prev_res:
			prev_res = result_to_color[result]
			os.system("..\\tools\\serial.exe COM6 " + prev_res)
		sleep(2)

if __name__ == "__main__":	
	jenkins = Jenkins(SERVER_URL)
	
	main()

#print("{} lastCompletedBuild: {} result: {} color: {}".format(JobName, last_completed_build_number, result, result_to_color[result]))


