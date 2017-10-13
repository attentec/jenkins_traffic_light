import requests
import random
import time

def genRandomPayload():
	for led in range(30):
		payload["led" + str(led)] = hex(random.randint(0,255))[2:].upper() + hex(random.randint(0,127))[2:].upper() + hex(random.randint(0,63))[2:].upper()

def updateLeds(payload):
	try:
		requests.post("http://192.168.28.85", data=payload, timeout=1)
	except  requests.exceptions.Timeout as e:
		pass

def turnOfAllLeds():
	global payload
	payload["quiet"] = "1"
	for led in range(30):
		payload["led" + str(led)] = "000000"
	updateLeds(payload)

def setProgress(percent):
	payload = {}
	ledsLighted = int(30 * (percent / 100))
	for led in range(30):
		if led <= ledsLighted:
			payload["led" + str(led)] = "0000FF"
		else:
			payload["led" + str(led)] = "000000"
	updateLeds(payload)