from scapy.all import sniff

# Dictionary to store IP-MAC mappings
IP_MAC_Map = {}

# Function to process each captured packet
def processPacket(packet):
    # Ensure the packet contains ARP layers
    if packet.haslayer('ARP'):
        src_IP = packet['ARP'].psrc
        src_MAC = packet['Ether'].src

        # Check if the MAC address is already in the map
        if src_MAC in IP_MAC_Map:
            # If the IP for the MAC address is different, it's suspicious
            if IP_MAC_Map[src_MAC] != src_IP:
                old_IP = IP_MAC_Map[src_MAC]
                message = (
                    "\nPossible ARP attack detected!\n"
                    f"The machine with IP address {old_IP} may be pretending to be {src_IP}.\n"
                )
                print(message)
        else:
            # Add the MAC-IP mapping to the dictionary
            IP_MAC_Map[src_MAC] = src_IP

# Start sniffing ARP packets
print("Sniffing for ARP packets... Press Ctrl+C to stop.")
sniff(filter="arp", store=False, prn=processPacket)
