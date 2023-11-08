#tj2557- PA1 Tharun Kumar Jayaprakash
import socket
import pickle  # This allows us to serialize data
from hashlib import md5 as md5

class UDPSocket:
    """
    This class abstracts socket communications from the Server and Client classes since the same code will be used by both.

    Methods:
        Constructor:
            Initializes the socket to listen on a specific PORT.
        send:
            Sends Python objects to the desired IP and Port using Pickle.
        secureSend:
            Sends data using a simple Stop and Wait Protocol.
        Receive:
            Waits for and receives a message, decodes it, and returns it.
        secureReceive:
            Receives data using a simple Stop and Wait protocol, working in conjunction with the secureSend method.

    Attributes:
        HOST: Holds the host IP.
        PORT: Holds the port number for sending and receiving data.
        socket: Facilitates communication.
    """
    def __init__(self, PORT, HOST='127.0.0.1'):
        # Here we specify the HOST IP and PORT
        self.HOST = HOST
        self.PORT = PORT
        # Create a UDP Socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set a timeout for the socket
        self.socket.settimeout(0.5)
        # Bind to the Port since both the Client and the Server need to be able to receive messages
        self.socket.bind((self.HOST, self.PORT))

    def secureSend(self, MSG, PORT, IP='127.0.0.1'):
        """
        This method securely sends data using the simple Stop and Wait Algorithm and a Checksum to ensure the integrity of the message.

        Parameters:
            MSG: A list with the following data in the respective indices:
                0th - Sequence Number of the Current Packet
                1st - The Command
                2nd - Message/Data to send

        What will be sent:
            A checksum will be sent before sending the message.
            A serialized list with the following information in its indices:
                0th - Sequence Number of the Current Packet
                1st - The Command
                2nd - Message/Data to send
                3rd - Checksum Hash

        Output:
            200 - if the message was sent successfully
            100 - if the message was not sent successfully
        """
        # We need to first pickle the message
        Data = pickle.dumps(MSG[2])
        # Calculate the Hash
        checksum = md5(Data).hexdigest()
        MSG.append(checksum)
        self.send(MSG, PORT, IP)
        # Start a timeout counter
        for i in range(5):
            try:
                ACK, _ = self.receive()
                if ACK == 'ACK':
                    # Everything went well, so we return 200
                    return 200
            except socket.timeout as e:
                print("Timed Out, will try again...")
                self.send(MSG, PORT, IP)
        # We tried multiple times, and it failed
        print("Message was not sent successfully")
        return 100

    def secureReceive(self):
        """
        This method is meant to receive data from a host securely in accordance with the secureSend() method. If the data is received correctly, the method will send an ACK back. If the data is not received correctly, the method will simply disregard the message.

        Output:
            100 -  if the data as not received correctly
            The data -  if the data was received correctly
        """
        # We want to continuously check for packets until we receive one
        while True:
            try:
                # Receive the Data
                rdata, Address = self.receive()
                if rdata != None:
                    break
            except socket.timeout as e:
                continue

        # Check the checksum
        dataToCheck = pickle.dumps(rdata[2])
        checksum = md5(dataToCheck).hexdigest()
        if len(rdata) >= 4:
            if checksum == rdata[3]:
                # Everything checks out!
                # We need to send an ACK
                # The Address Tuple is of the form (IP, PORT)
                self.send('ACK', Address[1], Address[0])
                # Return the Message to be processed
                return rdata[0:-1], Address

    def send(self, MSG, PORT, IP='127.0.0.1'):
        """
        This method sends a pickled object to the destination Port and IP.

        Parameters: 
            IP: The IP info of the Destination Host
            PORT: Destination Port number
        """
        MSG = pickle.dumps(MSG)
        self.socket.sendto(MSG, (IP, PORT))
            
    def receive(self):
        """
        This method receives pickled objects.
        """ 
        data, senderAddress = self.socket.recvfrom(20 * 1024)
        data = pickle.loads(data)
        return data, senderAddress
