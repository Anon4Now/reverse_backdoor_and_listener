# Reverse Backdoor & Listener

The contained files include the reverse backdoor script and the listener script needed for establishing a two-way connection.

## Disclaimer:
❗ **I DO NOT AUTHORIZE THE USE OF THESE FILES TO PERFORM ILLEGAL OR UNAUTHORIZED ACTIVITIES. ALL TESTS MUST BE PERFORMED ON DEVICES THAT ARE OWNED BY THE TESTER OR WITH THE EXPRESS WRITTEN CONSENT OF THE SYSTEM OWNER(S).**

## Tool Functionality:

- Will allow a backdoor to be created on the target machine with immediate persistance
- Will allow the attacker to perform standard CLI commands on the target (e.g. cd, dir, etc...)
- Will allow for upload/download to/from the target machine, this can be used for introducing other malware
- Will not launch a terminal window on the target machine, to avoid suspicion
- Will update the target machine's registry to execute the backdoor upon system restart
- Will store the executable in a non-conspicuous location 


## Tool Requirements:

- To use the default functionality of this tool, no additional libraries or modules are needed
- This tool needs a ![small](https://user-images.githubusercontent.com/80045938/148561762-9590c4a1-a424-4c7b-a0fb-68190fb7a31c.png) [Python](https://www.python.org/downloads/) interpreter, v3.6 or higher due to string interpolation


## Quick Notes:

- The attacker machine can be a Windows, OSX, or Linux OS
- The target machine is designed to be a Windows machine, however this can be altered if needed
- To get the needed python files on the target machine, the use of trojan's can be done or social engineering
- The target only need click the file once, and persistance will be created
- I wrote this with Python 2.7 capabilities as well, I commented out that code to avoid errors running in Python3



## Using the Tool:

#### Start the Listener: 
On the attacker machine, start the listener to await incoming connections.
![starting_listener](https://user-images.githubusercontent.com/80045938/149645661-fb2dda14-30f6-4853-b2cf-063bc222e9bf.gif)

#### Start the Backdoor: 
Use other red-team tactics to get the target to click the executable containing the python script (e.g. Trojan file).
![user_clicking_trojan](https://user-images.githubusercontent.com/80045938/149645686-2accbd71-90fa-41ba-86fd-6f667ec922ce.gif)

#### Check Connection from Listener: 
Watch for the incoming connection from target machine.
![connection_to_listener](https://user-images.githubusercontent.com/80045938/149645711-335b8c61-037f-4509-b740-f87f718812fa.gif)

#### Move Around on Target: 
An example of changing directories on the target.
![cd_dir](https://user-images.githubusercontent.com/80045938/149645741-28c19034-92ad-4598-b451-3ef0d2d544e2.gif)

#### Upload File to Target: 
An example of uploading a file to the target machine.
![upload_picture](https://user-images.githubusercontent.com/80045938/149645761-20d6f856-7434-4753-aed7-730a416c0cb9.gif)

#### Close the Connection From Listener: 
Watch for the incoming connection from target machine.
![exit_backdoor](https://user-images.githubusercontent.com/80045938/149645769-9780c105-8d95-453d-8420-3e04eecb4077.gif)


## Demonstration of Persistance on Target:

#### Hide the Executable:
The exe was dropped into C:\Users\<user>\AppData\Roaming\system1022.exe. 

App Roaming is hidden from users unless they edit the 'view' in file explorer to view all folders.
![persistance1](https://user-images.githubusercontent.com/80045938/149645804-09cff4d5-f460-4dfe-80b6-6ee5c8950041.jpg)


#### Update Target's Registry:
The HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run hive will be updated with a new key that will run the exe during start-up.
![persistance2](https://user-images.githubusercontent.com/80045938/149645838-e96cebd3-f77c-446f-907b-5ecdf3e727eb.jpg)
