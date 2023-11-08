from UDPSocket import UDPSocket
import time
from threading import Thread as th
import threading
from datetime import datetime
import pickle

class Server:
    
    def __init__(self, PORT):
        self.udp = UDPSocket(PORT)
        self.clientTable = dict()
        self.threads = []
        self.messages = dict()
        print("Server Online, Waiting for Users!")
        self.MainThread()

    def MainThread(self):
        while True:
            try:
                data, address = self.udp.secureReceive()
            except TypeError:
                continue
            if data != None:
                x = th(target=self.processMessage, args=(data, address), daemon=True)
                x.start()
                self.threads.append(x)
                data = None
                address = None

    # def processMessage(self, data, address):
    #     command = data[1].split(':')
    #     data = data[2]
    #     if command[0] == 'reg':
    #         self.registerUser(data, address[0], address[1])
    #     elif command[0] == 'dereg':
    #         self.deRegister(data)
    #     elif command[0] == 'MSG':
    #         self.storeMessage(command[1], data, address)
    #     elif command[0] == 'group':
    #         self.processGroupMessage(data, address)
    #     else:
    #         print("Incorrect Command")
    #         return None
    def processMessage(self, data, address):
        command = data[1].split(':')
        message = data[2]
        sender_nick = self.getNicknameFromAddress(address)

        if command[0] == 'reg':
            self.registerUser(message, address[0], address[1])
        elif command[0] == 'dereg':
            self.deRegister(message)
        elif command[0] == 'MSG':
        # Check if the message is sent from one user to themselves
            if sender_nick == message:
                self.sendMessageToSelf(sender_nick, message)
            else:
                self.storeMessage(command[1], message, address)
        elif command[0] == 'group':
            self.processGroupMessage(message, address)
        else:
            print("Incorrect Command")
            return None
        
    def sendMessageToSelf(self, sender_nick, message):
        # Handle the case where a user sends a message to themselves
        print(f"User {sender_nick} sent a message to themselves: {message}")

    def processGroupMessage(self, data, address):
        """
        This will process incoming group messages and send them to all clients.
        """
        sender_nick = self.getNicknameFromAddress(address)
        # Make sure the sender's nickname is in the clientTable
        if sender_nick in self.clientTable:
            group_message = data
            # Send the group message to all registered clients except the sender
            self.sendGroupMessage(sender_nick, group_message)
        else:
            print("Sender not in clientTable")

    def sendGroupMessage(self, sender_nick, message):
        """
        This sends a group message to all registered clients except the sender.
        """
        for nick, clientData in self.clientTable.items():
            # Skip the sender
            if nick == sender_nick:
                continue
            IP = clientData['IP']
            PORT = clientData['PORT']
            online = clientData['Online']
            group_message = [1, 'MSG:' + sender_nick, message]
            if online:
                response = self.udp.secureSend(group_message, PORT, IP)
                if response == 200:
                    # Message sent successfully to the online client
                    print("Group message sent to:", nick)
            else:
                # Store the message for offline clients
                if nick in self.messages:
                    self.messages[nick].append(group_message)
                else:
                    self.messages[nick] = [group_message]
                print("Group message stored for offline client:", nick)

    def getNicknameFromAddress(self, address):
        """
        Get the nickname of a client from their IP and Port.
        """
        for nick, clientData in self.clientTable.items():
            if clientData['IP'] == address[0] and clientData['PORT'] == address[1]:
                return nick
        return None

    def registerUser(self, nick, IP, PORT):
        client = dict()
        client['Nick'] = nick  # Added the 'Nick' key
        client['IP'] = IP
        client['PORT'] = PORT
        client['Online'] = True
        self.clientTable[nick] = client
        print("Registered {} at {}:{}".format(nick, IP, PORT))
        self.updateAllClients()
        self.sendStored(nick)

    def updateAllClients(self):
        MSG = [1, 'update:', self.clientTable]
        for client, clientData in self.clientTable.items():
            PORT = clientData['PORT']
            IP = clientData['IP']
            if clientData['Online'] == True:
                response = self.udp.secureSend(MSG, PORT, IP)
        print("Updated All Clients")

    def deRegister(self, nick):
        self.clientTable[nick]['Online'] = False
        PORT = self.clientTable[nick]['PORT']
        IP = self.clientTable[nick]['IP']
        self.udp.secureSend([1, 'ACK'], PORT, IP)
        self.updateAllClients()

    def sendStored(self, nick):
        if nick in self.messages:
            for stored_message in self.messages[nick]:
                message = [1, 'MSG:', stored_message]
                IP = self.clientTable[nick]['IP']
                PORT = self.clientTable[nick]['PORT']
                self.udp.secureSend(message, PORT, IP)

if __name__ == '__main__':
    server = Server(50000)