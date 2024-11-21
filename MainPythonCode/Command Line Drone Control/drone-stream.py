#they won't give it to us, so it's our turn to figure out how to turn the cameras on, on the drone.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)  # Drone IP address
sock.bind(('', 11111))

#Get the user to type streamon to start stream connection
while True:
    try: 
        msg = input("Enter command: ")
        if 'streamon' in msg:
            break
    print("You need to type 'streamon' to start stream connection")

# Continuously send commands typed in by the user
while True:
    try:
        msg = input("Enter command: ")
        if 'end' in msg:
            sock.close()
            break
        elif 'streamon' in msg:
            
        sock.sendto(msg.encode(), tello_address)
    except Exception as e:
        print(f"Error: {e}")
        sock.close()
        break