from jenkins import Jenkins
import pprint
import os
import serial
import argparse
from time import sleep


result_to_color={'SUCCESS': b'G',
                 'UNSTABLE': b'Y',
                 'FAILURE': b'R'}

SERVER_URL='http://ci.attentec.se'
JOB_NAME = 'Hacka-Traffic-Light'


def get_jenkins_build_info(jenkins, job_name, build_type):
	jobs = jenkins.get_job_info(job_name, 0, False)
	job = jobs[build_type]
	build_number = job["number"]
	build_info = jenkins.get_build_info(JOB_NAME, build_number) 
	return build_info

def connectToSerialPort(_port, _baudrate):
	return serial.Serial(
	    port= _port,
	    baudrate= _baudrate,
	    parity=serial.PARITY_NONE,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS,
	    rtscts=False,
	    dsrdtr=False)

def main(_port, _baudrate):
	prev_res = ""
	ser = connectToSerialPort(_port, _baudrate)

	while True:		
		build_info = get_jenkins_build_info(jenkins, JOB_NAME, "lastCompletedBuild")
		result = build_info["result"]
		if result_to_color[result] != prev_res:
			prev_res = result_to_color[result]
			ser.write(prev_res)
		sleep(2)

if __name__ == "__main__":	
	parser = argparse.ArgumentParser()
	parser.add_argument("port")
	parser.add_argument("--baudrate", default=115200, type=int)
	args = parser.parse_args()
	jenkins = Jenkins(SERVER_URL)
	main(args.port, args.baudrate)

#print("{} lastCompletedBuild: {} result: {} color: {}".format(JobName, last_completed_build_number, result, result_to_color[result]))


