import socket

# Setup the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8890))

# Continuously listen for state messages from the drone
while True:
    try:
        data, server = sock.recvfrom(1024)
        status = data.decode()
        print(f"Received: {status}")
    except Exception as e:
        print(f"Error: {e}")
        sock.close()
        break