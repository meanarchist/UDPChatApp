#tj2557- PA1 Tharun Kumar Jayaprakash
# This is the main program that runs both the Server and the Client based on the inputs given when running the script

import sys  # This handles the command line arguments
from Server import Server
from Client import Client

"""
The Arguments are taken in the following form:

Server:
    -s <Port>
Client:
    -c <nick-name> <server-IP> <server-Port> <client-Port>
"""

def Main(arguments):
    """
    This method uses the system arguments to run the correct script and input the parameters to the program.
    """
    if arguments[0] == '-s':
        if len(arguments) > 2:
            print("Too many Arguments!")
        elif len(arguments) < 2:
            print("Not enough Arguments")
        else:
            print("Starting the Server")
            server = Server(int(arguments[1]))
    elif arguments[0] == '-c':
        if len(arguments) < 5:
            print("Not Enough Arguments!")
        elif len(arguments) > 5:
            print("Too many Arguments")
        else:
            nick = arguments[1]
            serverIP = arguments[2]
            serverPort = int(arguments[3])
            clientPort = int(arguments[4])
            client = Client(nick, '127.0.0.1', clientPort, serverPort, serverIP)
    else:
        print("Wrong arguments")
    return None

if __name__ == '__main__':
    Main(sys.argv[1:])
