import socket

from djitellopy import Tello

tello = Tello()

tello.connect()

# Setup the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)  # Drone IP address
sock.bind(('', 9000))
print("Current Battery Level:", tello.get_battery())
# Continuously send commands typed in by the user
while True:
    try:
        msg = input("Enter command: ")
        if 'end' in msg:
            sock.close()
            break
        sock.sendto(msg.encode(), tello_address)
    except Exception as e:
        print(f"Error: {e}")
        sock.close()
        break