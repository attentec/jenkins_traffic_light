#include "windows.h"
#include "stdio.h"
#include "string.h"

typedef unsigned char U8;
/*typedef enum {
	FALSE,
	TRUE
} BOOL;*/

HANDLE comPort;

BOOL ConnectToCom(char *comPortName) {
	DCB dcbStr;

	comPort = CreateFile(comPortName,  
                    GENERIC_READ | GENERIC_WRITE, 
                    0, 
                    0, 
                    OPEN_EXISTING,
                    0,
                    0);

	if (comPort == INVALID_HANDLE_VALUE) {
		printf("Could not open port: %s\n", comPortName);
		return FALSE;
	}

	if (!GetCommState(comPort, &dcbStr)) {
		printf("GetCommState failed\n");
		return FALSE;
	}

	dcbStr.BaudRate = CBR_115200;
	dcbStr.DCBlength = sizeof(dcbStr);
	dcbStr.ByteSize = 8;

	if (!SetCommState(comPort, &dcbStr)) {
		printf("SetCommState failed\n");
		return FALSE;
	}

	return TRUE;
}

BOOL WriteToCom(char bytesToWrite[], U8 numberOfBytes) {
	DWORD bytesWritten = 0U;

	if (WriteFile(comPort, ((void*)bytesToWrite), (DWORD)numberOfBytes, &bytesWritten, NULL)) {
		printf("Wrote %lu bytes successfully\n", bytesWritten);
	}
	else {
		printf("Write failed with error: %lu\n", GetLastError());
		return FALSE;
	}

	return TRUE;
}

BOOL ReadFromCom(char buffer[], U8 numberOfBytesToRead) {
	DWORD bytesRead = 0;

	if (ReadFile(comPort, ((void*)buffer), (DWORD)numberOfBytesToRead, &bytesRead, NULL)) {
		printf("Read success\n");
	}
	else {
		printf("Read failed with error: %lu\n", GetLastError());
		return FALSE;
	}

	return TRUE;
}


int main (int argc, char **argv) {
	char comPortName[64U];
	char message[64U];
	char response[64U];
	U8 messageLength;

	if (argc < 2) {
		printf("Missing com port and message\n");
	}
	else if (argc < 3) {
		printf("Missing message\n");
	}

	strcpy(comPortName, argv[1]);
	strcpy(message, argv[2]);

	messageLength = strlen(message);

	if (ConnectToCom(comPortName)) {
		if (WriteToCom(message, messageLength)) {
			if(ReadFromCom(response, messageLength)) {
				return 0;
			}
			else {
				return 1;
			}
		}
	}	
	return 0;
}