import requests
import random
import time
from threading import Thread
from queue import Queue, Empty

q = Queue()

def genRandomPayload(payload):
	for led in range(30):
		payload["led" + str(led)] = hex(random.randint(0,255))[2:].upper() + hex(random.randint(0,127))[2:].upper() + hex(random.randint(0,63))[2:].upper()

def updateLeds(payload):
	try:
		requests.post("http://192.168.28.85", data=payload, timeout=1)
	except  requests.exceptions.Timeout as e:
		pass

def startUpThread():
	t = Thread(target=worker, args=(q,))
	t.start()

def killThread():
	q.put(("kill"))

def turnOfAllLeds():
	payload = {"quiet": "1"}
	for led in range(30):
		payload["led" + str(led)] = "000000"
	updateLeds(payload)

def setProgress(percent):
	q.put(("percent", percent))

def setLedsSuccess():
	payload = {"quiet": "1"}
	for led in range(30):
		payload["led" + str(led)] = "00FF00"
	updateLeds(payload)

def setLedsFail():
	payload = {"quiet": "1"}
	for led in range(30):
		payload["led" + str(led)] = "FF0000"
	updateLeds(payload)

def setLedsUnstable():
	payload = {"quiet": "1"}
	for led in range(30):
		payload["led" + str(led)] = "FFFF00"
	updateLeds(payload)

def worker(q):
	ledsLighted = 0
	p = {"quiet": "1"}
	blinkingLedOn = True
	while True:
		try:
			item = q.get(timeout=0.5)
			if item[0] == "percent":
				ledsLighted = int(30 * (int(item[1]) / 100))
			elif item[1] == "kill":
				return
		except Empty as e:
			pass

		blinkingLed = ledsLighted + 1
		for led in range(30):
			if led <= ledsLighted:
				p["led" + str(led)] = "0000FF"
			else:
				p["led" + str(led)] = "000000"

		if blinkingLedOn:
			p["led" + str(blinkingLed)] = "000000"
			blinkingLedOn = False
		else:
			p["led" + str(blinkingLed)] = "0000FF"
			blinkingLedOn = True

		updateLeds(p)
