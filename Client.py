#tj2557- PA1 Tharun Kumar Jayaprakash
#This file will hold all the code needed by the Client in for the UDP Chat

from UDPSocket import UDPSocket
from threading import Thread as th
import sys
from datetime import datetime

class Client:
    def __init__(self, Nick, IP, PORT, ServerPort, ServerIP='127.0.0.1'):
        self.threads = []
        self.Nick = Nick
        self.serverPort = ServerPort
        self.serverIP = ServerIP
        self.udp = UDPSocket(PORT, IP)
        self.clientTable = dict()
        print("Initializing Connection with Server...")
        response = self.udp.secureSend([1, "reg:", Nick], ServerPort, ServerIP)
        if response != 200:
            print("We didn't connect to the Server")
            return None
        print("We successfully connected to the Server!\n")
        print("Waiting for the updated table of Clients")
        while True:
            try:
                data, Address = self.udp.secureReceive()
                if data is not None:
                    break
            except TypeError:
                continue
        if data[2] == "ERROR":
            print("Nickname is already taken. Please Try Again.")
            exit()
        self.clientTable = data[2]
        print("Received the Table of other Clients!")
        print(self.clientTablePrint())
        self.MainLoop()

    def clientTablePrint(self):
        nicknames = self.clientTable.keys()
        names = 'Clients:|Status:\n--------------\n'
        for nick in nicknames:
            online = self.clientTable[nick]['Online']
            if online:
                online = 'Online'
            else:
                online = 'Offline'
            names += '{} | {}\n'.format(nick, online)
        return names

    def MainLoop(self):
        y = th(target=self.processInput, daemon=True)
        y.start()
        self.threads.append(y)
        while True:
            try:
                data, address = self.udp.secureReceive()
            except TypeError:
                continue
            if data is not None:
                x = th(target=self.processMessage, args=(data, address), daemon=True)
                x.start()
                self.threads.append(x)
                data = None
                address = None
        return None

    def processMessage(self, data, address):
        command = data[1].split(':')
        data = data[2]
        if command[0] == 'update':
            self.clientTable = data
        elif command[0] == 'MSG':
            if address[1] == self.serverPort:
                print(">>> You Have Messages")
            print('>>> {} {}'.format(datetime.now(), data))
        elif command[0] == 'group':
            # Handle group chat messages
            sender = data.split(':')[0]
            message = data[len(sender) + 1:]
            print('Group chat from {}: {}'.format(sender, message))
        else:
            print('>>> Incorrect Command. Please Try Again')

    def processInput(self):
        while True:
            command = input(">>> ").split(' ')
            if command[0] == 'send':
                if command[1] == 'group':
                    self.sendGroupMessage(" ".join(command[2:]))
                else:
                    nick = command[1]
                    data = " ".join(command[2:])
                    #self.sendMessage(nick, data)
                    if nick == self.Nick:  # Handle the case where a client sends a message to themselves
                        self.sendMessageToSelf(data)
                    else:
                        self.sendMessage(nick, data)
            elif command[0] == 'clients':
                print(self.clientTablePrint())
            elif command[0] == 'dereg':
                MSG = [1, 'dereg:', self.Nick]
                self.udp.secureSend(MSG, self.serverPort, self.serverIP)
                data, _ = self.udp.secureReceive()
                if data[2] == 'ACK':
                    print("You're Offline.")
                    sys.exit()
                else:
                    print("Server Connection Timed Out\n")
                    print("Exiting...")
                    sys.exit()
            else:
                print(">>> Unknown command. Please try again.")

    
    def sendMessageToSelf(self, data):
    # Handle the case where a client sends a message to themselves
        print('>>> You sent a message to yourself:', data)
    

    def sendMessage(self, nick, MSG):
        if nick not in self.clientTable:
            print(">>> No Record of that Client. Please try again!")
            return None

        IP = self.clientTable[nick]['IP']
        PORT = self.clientTable[nick]['PORT']

        MSG = [1, 'MSG:' + nick, self.Nick + ": " + MSG]

        if not self.clientTable[nick]['Online']:
            response = self.udp.secureSend(MSG, self.serverPort, self.serverIP)
            if response == 200:
                print("Your Message was Successfully Saved in the Server!")
                return None
            else:
                print("There was an error sending the message to the Server")
        else:
            response = self.udp.secureSend(MSG, PORT, IP)
            if response == 200:
                return None
            else:
                response = self.udp.secureSend(MSG, self.serverPort, self.serverIP)
                if response == 200:
                    print("Client was offline. Sent the message to the Server")
                    data, _ = self.udp.secureReceive()
                    if data[1] == 'ERROR':
                        print(data[2])

    def sendGroupMessage(self, MSG):
        group_message = [1, 'group', MSG]
        response = self.udp.secureSend(group_message, self.serverPort, self.serverIP)
        if response == 200:
            print("Your Group Message was Successfully Sent!")
        else:
            print("There was an error sending the group message")

if __name__ == '__main__':
    client = Client('Buddy', '127.0.0.1', 50020, 50000)