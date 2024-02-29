import random
import socket
import time
from random import randint

# client inside the IS and who sends legal system info to the second client

SECOND_CLIENT_ADDRESS = ('127.0.0.1', 65012)
FIRST_CLIENT_ADDRESS = ('127.0.0.1', 65011)
PROXY_ADDRESS = ('127.0.0.1', 65010)

print("Client 1 has started")


soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind(FIRST_CLIENT_ADDRESS)


def sender():
    while True:
       try:
          time_parameter = random.uniform(2, 3)
          #buffer = random.randbytes(randint(1024, 2048))
          buffer = "Hello world"
          soc.sendto(buffer.encode(), PROXY_ADDRESS)
          #soc.sendto(buffer, PROXY_ADDRESS)
          time.sleep(time_parameter)
       except (KeyboardInterrupt, EOFError) as e:
          soc.close()
          break

if __name__ == '__main__':
    sender()
