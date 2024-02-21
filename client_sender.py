import socket
import threading
import platform
import time

# client inside the IS and who sends legal system info to the second client

SECOND_CLIENT_ADDRESS = ('::1', 65012, 0, 0)
FIRST_CLIENT_ADDRESS = ('::1', 65011, 0, 0)
PROXY_ADDRESS = ('::1', 65010. 0, 0)

print("Client 1 has started")
time_parameter = 5


soc = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
soc.bind(FIRST_CLIENT_ADDRESS)


def listener():
    for i in range(100):
        buffer = "Hello world"
        soc.sendto(buffer.encode(), PROXY_ADDRESS)


if __name__ == '__main__':
    listener()
    soc.close()
