# UDP Chat Application - ReadMe

## Introduction

This README provides an overview of the UDP Chat Application, which serves as a basic chat system for communication between clients via UDP (User Datagram Protocol). This application is designed to demonstrate essential networking concepts and features, including direct messaging, group chat, message persistence, and offline message delivery.

## Features

The UDP Chat Application includes the following key features:

1. **Direct Messaging:** Users can send direct messages to one another within the chat system. Messages are delivered between clients in real-time.

2. **Group Chat:** The application supports group chat, allowing multiple clients to participate in the same conversation.

3. **Offline Message Delivery:** Even if a client is temporarily offline, the system will store messages for them. When the client logs back in, any missed messages are delivered.

4. **Server Handling:** The server keeps an accurate client table, tracks online/offline status, and manages message delivery.

5. **Sending Messages to Self:** Users can send messages to themselves without any issues.

6. **Timeout Handling:** The application incorporates timeout mechanisms to ensure message delivery and handle acknowledgment (ACK) failures.

7. **Server Recovery:** In case the server goes offline, it is designed to handle deregistration requests and allow clients to continue sending messages to each other.

## Usage

To use the UDP Chat Application, follow these steps:

### Server
1. Run the server by specifying the desired port:

```python UDPClient.py -s <Port>```

**OR**

1. Run the server application by running server.py(by default, port 5000 is utilised)

### Client
1. Run a client by specifying your nickname, server IP, server port, and client port:
```python UDPClient.py -c <Nickname> 127.0.0.1 <Server-Port> <Client-Port>```

2. Start chatting! Use commands such as `send`, `group`, `dereg`, and `clients` to interact with other clients.

## Additional Test Cases

In addition to the test cases provided in the PA1 handout, two additional test cases have been implemented to ensure the application's functionality.

### Test Case 1: Offline Message Delivery
- Simulate sending messages to an offline user.
- Verify that the offline user receives the messages upon re-registration.

### Test Case 2: Server Recovery
- Simulate the server going offline.
- Verify that the application handles this scenario correctly and allows clients to continue communicating.

## Performance Considerations

The application has been optimized to ensure smooth performance. However, if you experience any performance issues or notice jumbled output, please report them for further investigation.

## Author and Contact

- Tharun Kumar Jayaprakash(tj2557)
- tj2557@columbia.edu

