from scapy.all import *
import socket

# client outside the IS who recieves the legal info as well as secrete message that was added by proxy

SECOND_CLIENT_ADDRESS = ('127.0.0.1', 65012)
FIRST_CLIENT_ADDRESS = ('127.0.0.1', 65011)
PROXY_ADDRESS = ('127.0.0.1', 65010)


K = 64
W = 8
SEED = 12345678

print("Client 2 has started")

random.seed(SEED)

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp - "socket.SOCK_DGRAM", tcp - Stream
soc.bind(SECOND_CLIENT_ADDRESS)
soc.connect(PROXY_ADDRESS)  	 

def listener():
    cur_i = 0
    bits_of_msg = ''
    while True:
        data = soc.recv(1024)
        #print(len(data))
        msg = data.decode('utf-8') 
        print(msg)
        #bits_of_msg += decoder(data, cur_i)
        cur_i += 1
        #bits_of_msg = '01001000011001010110110001101100011011110010110000100000011101000110100001101001011100110010000001101001011100110010000001110110011001010111001001111001001000000111001101100101011000110111001001100101011101000010000001101001011011100110011001101111011100100110110101100001011101000110100101101111011011100010110000100000011000110110000101101110001000000111100101101111011101010010000001101011011001010110010101110000001000000110000100100000011100110110010101100011011100100110010101110100001011000010000001110100011010000110010100100000011100000110000101110011011100110111011101101111011100100110010000110001'
        if cur_i == K // W:
            bits_of_msg += decoder(data, cur_i)
            print('Bits of msg:', bits_of_msg)
            print('Decoded msg:', ''.join([chr(int(bits_of_msg[i:i+8], 2)) for i in range(0, len(bits_of_msg), 8)]))
            break
	
def decoder(msg, cur_i):
    l_next = len(msg)
    l_max = 0
    all_ls = []
    with open('Dictionary.txt', 'r') as f:
        all_ls = f.read().split('\n')
        l_max = int(all_ls[cur_i])
    sum_i = l_next - l_max
    w_i = sum_i
    if cur_i % 2 == 0:
        w_i += 2 ** (W - 1)
    else:
        w_i += (2 ** (W - 1) - 1)
    return format(w_i, f'0{W}b')

if __name__ == '__main__':
    listener()