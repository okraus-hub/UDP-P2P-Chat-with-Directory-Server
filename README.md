# UDP-P2P-Chat-with-Directory-Server
This project implements a simple peer-to-peer (P2P) chat application using UDP sockets in Python. A central directory server handles user registration and lookup, allowing clients to connect and communicate directly.

## Features
- Peer-to-peer communication over UDP
- Lightweight directory server for user discovery
- Multi-threaded client for concurrent message sending and receiving
- Basic fault tolerance in user lookup with retries

## Project Structure
- chatP2.py: Client script to initiate chat sessions
- directory_server.py: Central server that registers users and resolves their addresses

## How It Works
1. **Registration**: Each client registers with the directory server by sending its username, IP, and port.
2. **Lookup**: To chat, the client looks up the destination username to retrieve their IP and port.
3. **Chat**: Once resolved, the clients communicate directly using UDP messages.

## Requirements
- Python 3.x
  
## Usage
- To test the chat application, you'll need at least two terminals — one for the directory server and others for the chat clients.
1. Start the Directory Server: python directory_server.py [port]
   [EX] python directory_server.py 4000
2. Start Client 1: python chatP2.py <your_username> <your_ip:your_port> <destination_username> <dir_ip:dir_port>
   [EX] python chatP2.py alice 127.0.0.1:5001 bob 127.0.0.1:4000
3. Start Client 2 (in second terminal): python chatP2.py <your_username> <your_ip:your_port> <destination_username> <dir_ip:dir_port>
   [EX] python chatP2.py bob 127.0.0.1:5002 alice 127.0.0.1:4000

##Exiting
-To exit, press Ctrl+C in client terminal
