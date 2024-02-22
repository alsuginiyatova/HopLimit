from scapy.all import *
import socket
import argparse
import queue
from bitarray import bitarray

# client outside the IS who recieves the legal info as well as secrete message that was added by proxy

SECOND_CLIENT_ADDRESS = ('::1', 65012, 0, 0)
FIRST_CLIENT_ADDRESS = ('::1', 65011, 0, 0)
PROXY_ADDRESS = ('::1', 65010, 0, 0)


print("Client 2 has started")


soc = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)  # udp - "socket.SOCK_DGRAM", tcp - Stream
soc.bind(SECOND_CLIENT_ADDRESS)
soc.connect(PROXY_ADDRESS)


class MyConcurrentCollection:
    def __init__(self):
        self.collection = queue.Queue()

    def append(self, x):
        self.collection.put(x)

    def pop(self):
        return self.collection.get()

    def __len__(self):
        return self.collection.qsize()

    def __str__(self):
        return f"{len(self)}"

    def print_collection(self):
        return self.collection.queue

    def empty(self):
        return self.collection.empty()

class Worker(threading.Thread):
    def __init__(self, input_collection: MyConcurrentCollection, callback=None):
        if not callback:
            raise NameError('callback not set')

        threading.Thread.__init__(self)
        self.daemon = True
        self.msg = []
        self.input_collection = input_collection
        self.callback = callback

    def run(self):
        sleep_time = 0
        while True:
            if not self.input_collection.empty():
                print("Run sniff")
                packet = self.input_collection.pop()

                msg_i = self.callback(packet)
                if not msg_i == -1:
                    self.msg.append(msg_i)

            else:
                time.sleep(0.1)
                sleep_time += 0.1
                if sleep_time > 5.0:
                    self.msg = self.msg[::2]
                    print(self.msg)
                    return
                    
    def bits_to_string(self):
        try:
            # Создаем объект bitarray из списка битов
            bit_array = bitarray(self.msg)
            # Преобразуем bitarray в байтовую строку
            byte_string = bit_array.tobytes()
            # Преобразуем байтовую строку в строку с использованием кодировки UTF-8
            result = byte_string.decode('utf-8')
            print("Message:")
        except:
            print('Error in convert bits msg to string')
            result = self.msg
        return result
                   
class Agent:
    def __init__(self, callback=None, threads_count = 1):
        self.col = MyConcurrentCollection()
        self.consumers = [Worker(self.col, callback) for _ in range(threads_count)]


    def sniffer(self):
        print("run sniff")
        sniff(filter="src port 65011 and dst port 65012", prn=self.col.append, iface="lo")


    def run(self):
        for consumer in self.consumers:
            consumer.start()

        self.sniffer()

        for consumer in self.consumers:
            consumer.join()        

def listener():
    while True:
        msg = soc.recv(1024).decode('utf-8')
        print(msg)


def decoder_hop_limit(pac):
    if pac.hlim == 5:
        return 1
    elif pac.hlim == 105:
        return 0
    return -1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Covert channel emulation')
    parser.add_argument('covert_mode', default='hop_limit', const='hop_limit', nargs='?', choices=['hop_limit'])
    args = parser.parse_args()
    match args.covert_mode:
        case "hop_limit":
            callback = decoder_hop_limit

    agent = Agent(callback)
    thread_agent = threading.Thread(target=agent.run, args=())
    thread_proxy = threading.Thread(target=listener, args=())
    
    thread_agent.start()
    thread_proxy.start()
    
    thread_agent.join()
    thread_proxy.join()

