#import socket
#import threading
#import argparse
#import bitarray
#import queue
#from scapy.all import *
#from scapy.layers.inet import *

from scapy.all import *
import socket
import argparse
import queue
from scapy.layers.inet import *


SECOND_CLIENT_ADDRESS = ('127.0.0.1', 65012)
FIRST_CLIENT_ADDRESS = ('127.0.0.1', 65011)
PROXY_ADDRESS = ('127.0.0.1', 65010)
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind(PROXY_ADDRESS)

SEED = 12345678

random.seed(SEED)


K=64
W=8


# Имитация сетевого экрана
def listener():

    while True:
        data, address = soc.recvfrom(1024)
        if address[1] == 65011:
            soc.sendto(data, SECOND_CLIENT_ADDRESS)
        if address[1] == 65012:
            soc.sendto(data, FIRST_CLIENT_ADDRESS)


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
    def __init__(self, msg, input_collection: MyConcurrentCollection, callback=None):
        if not callback:
            raise NameError('callback not set')

        threading.Thread.__init__(self)
        self.daemon = True
        self.msg = ''.join(format(ord(x), '08b') for x in msg)
        self.input_collection = input_collection
        self.callback = callback
        self.i = 0

    def run(self):
        print(self.msg)
        while True:
            if len(self.msg) == 0:
                print("Covert channel close, all message send")
                return 
            #if not self.input_collection.__len__() > 0:
            if not self.input_collection.empty():
                print(self.i // W)
                print(self.input_collection.pop())
                packet = self.input_collection.pop()
                if self.i == 0:
                   with open('Dictionary.txt', 'w') as f:
                      print('okey')
                      pass
                covert_message = self.msg[:W]
                self.msg = self.msg[W:]
                self.callback(covert_message, packet, self.i) 
                self.i += W
            else:
                time.sleep(0.1)
                   

class Agent:
    def __init__(self, msg, callback=None, threads_count = 1):
        self.col = MyConcurrentCollection()
        self.consumers = [Worker(msg, self.col, callback) for _ in range(threads_count)]


    def sniffer(self):
        print("run sniff")
        sniff(filter="src port 65011 and dst port 65010", prn=self.col.append, iface="lo0")


    def run(self):
        for consumer in self.consumers:
            consumer.start()

        self.sniffer()

        for consumer in self.consumers:
            consumer.join()

def calc_sum_i(cur_i, w_i):
    sum_i = 0

    if cur_i % 2 == 0:
       sum_i += int(w_i, 2) - 2 ** (W - 1)
    else:
       sum_i += int(w_i, 2) - (2 ** (W - 1) - 1)

    return sum_i

def covert(covert_message, pkt, i):
    if i == 0:
       with open('Dictionary.txt', 'a+') as f:
           l_max = random.randrange(2 ** W + 1, 3 ** W)
           cur_l = l_max
           l_next = cur_l
           print(str(l_max))
           f.write(str(l_max) + '\n')
           #msg_to_send = ' ' * l_next 
           #soc.sendto(msg_to_send.encode(), SECOND_CLIENT_ADDRESS)
    else:
       with open('Dictionary.txt', 'r') as f:
           print('a')
           all_ls = f.read().split('\n')[:-1]
           l_max = int(all_ls[0])
           #l_next = int(random.choice(all_ls))
           l_next = int(all_ls[len(all_ls) - 1])
           cur_l = l_next
       
    cur_l = l_next
    sum_i = calc_sum_i(i // W, covert_message)
    l_next = sum_i + cur_l if sum_i + cur_l > 0 else sum_i + cur_l + l_max

    with open('Dictionary.txt', 'a') as f:
        f.write(str(l_next) + '\n')

    msg_to_send = ''.join(random.choices(string.ascii_letters, k=l_next))
    l_max = cur_l
    time.sleep(random.uniform(2,3))

    soc.sendto(msg_to_send.encode(), SECOND_CLIENT_ADDRESS)
    print(len(msg_to_send))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Covert channel emulation')
    parser.add_argument('-f', '--filename', help='data to tranfer via covert channel', required=False, dest='filename', type=str)
    args = parser.parse_args()
    if args.filename:
        file = open(args.filename)
        msg = file.read()
    else:
        msg = input()
    try:
        #ba = bitarray.bitarray()
        #ba.frombytes(msg.encode('utf-8'))
        #msg = ba.tolist()
        agent = Agent(msg, covert)
        thread_agent = threading.Thread(target=agent.run, args=())
        thread_proxy = threading.Thread(target=listener, args=())
    
        thread_agent.start()
        thread_proxy.start()
       
        thread_agent.join()
        thread_proxy.join()
        #sniff()
    except (KeyboardInterrupt, EOFError) as e:
       pass
