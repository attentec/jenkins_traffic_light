import serial
import argparse
from pprint import pprint

parser = argparse.ArgumentParser(description='Send over serial.')
parser.add_argument('--port', help='the serial port')
parser.add_argument('--string', help='the string to send')

args = parser.parse_args()

ser = serial.Serial(args.port, 115200)  # open serial port
print(ser.name)         # check which port was really used
ser.write(args.string)     # write a string
ser.close()