import json
import socket
import sys

#Directory mapping usernames to (IP, Port)
user_directory = {}

#Set up UDP server, user specifies port if they want
server_ip = "0.0.0.0"
server_port = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip, server_port))

print(f"Directory service running on {server_ip}:{server_port}")

while True:
    try: 
        data, addr = sock.recvfrom(4096)
        request = json.loads(data.decode())
        response = {}

        if "UID" in request and "user IP" in request and "user PORT" in request:
            try:
                user_directory[request["UID"]] = (request["user IP"], int(request["user PORT"]))  # Ensure PORT is int
                response = {"error code": 400, "message": "Registration successful"}
                print(f"Registered: {request['UID']} -> {request['user IP']}:{request['user PORT']}")
            except ValueError:
                response = {"error code": 600, "message": "Invalid port number"}
        elif "target" in request and "user" in request:
            target = request["target"]
            if target in user_directory:
                response = {
                    "error code": 400,
                    "destination IP": user_directory[target][0],
                    "destination port": user_directory[target][1],
                }
                print(f"Lookup success: {target} -> {response['destination IP']}:{response['destination port']}")
            else:
                response = {"error code": 600}
                print(f"Lookup failed: {target} not found")
            
        sock.sendto(json.dumps(response).encode(), addr)
    except Exception as e:
        print("Error handling request:", e)
