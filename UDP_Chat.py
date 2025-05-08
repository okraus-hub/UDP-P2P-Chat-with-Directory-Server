import sys
import json
import socket
import threading
import time

if len(sys.argv) != 5:
    print("Usage: python chatP2.py <username> <host_ip:port> <destination_user> <dir_ip:port>")
    sys.exit(1)

username = sys.argv[1]
host_ip, host_port = sys.argv[2].split(":")
destination_user = sys.argv[3]
dir_ip, dir_port = sys.argv[4].split(":")
host_port, dir_port = int(host_port), int(dir_port)
400
# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host_ip, host_port))

def register_with_directory():
    registration_message = {
        "UID": username,
        "user IP": host_ip,
        "user PORT": host_port,
    }
    sock.sendto(json.dumps(registration_message).encode(), (dir_ip, dir_port))
    response, _ = sock.recvfrom(4096)
    response_data = json.loads(response.decode())
    if response_data.get("error code") == 400:
        print("Registration successful!")
    else:
        print("Registration failed.")
        sys.exit(1)

def lookup_destination():
    lookup_message = {"target": destination_user, "user": username}
    while True:
        sock.sendto(json.dumps(lookup_message).encode(), (dir_ip, dir_port))
        response, _ = sock.recvfrom(4096)
        response_data = json.loads(response.decode())

        if response_data.get("error code") == 400:
            if "destination IP" in response_data and "destination port" in response_data:
                return response_data["destination IP"], response_data["destination port"]
            else:
                print("Server response missing necessary fields. Retrying in 5 seconds...")
        else:
            print("User not found. Retrying in 5 seconds...")

        time.sleep(5)

def receive_messages():
    while True:
        try:
            data, _ = sock.recvfrom(4096)
            message = json.loads(data.decode())
            print(f"{message['UID']}>> {message['Message']}")
        except Exception as e:
            print("Error receiving message:", e)

# Register and lookup destination user
register_with_directory()
dest_ip, dest_port = lookup_destination()
print(f"Chatting with {destination_user} at {dest_ip}:{dest_port}")

# Start receiver thread
threading.Thread(target=receive_messages, daemon=True).start()

# Sending messages
while True:
    try:
        msg = input().strip()
        if not msg:
            continue
        message_dict = {
            "Version": "v1",
            "UID": username,
            "DID": destination_user,
            "Message": msg,
        }
        sock.sendto(json.dumps(message_dict).encode(), (dest_ip, dest_port))
    except KeyboardInterrupt:
        print("\nExiting chat...")
        break
    except Exception as e:
        print("Error sending message:", e)

sock.close()
