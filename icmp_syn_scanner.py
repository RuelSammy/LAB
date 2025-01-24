from scapy.all import IP, ICMP, TCP, sr1, sr # type: ignore
import sys

def icmp_probe(ip):
    """Send an ICMP packet to check if the host is reachable."""
    print(f"Performing ICMP probe to {ip}...")
    icmp_packet = IP(dst=ip) / ICMP()
    resp_packet = sr1(icmp_packet, timeout=10, verbose=False)
    return resp_packet is not None

def syn_scan(ip, port):
    """Perform a SYN scan on the specified IP and port."""
    print(f"Performing SYN scan on {ip}:{port}...")
    syn_packet = IP(dst=ip) / TCP(dport=int(port), flags="S")
    resp = sr1(syn_packet, timeout=10, verbose=False)
    return resp

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <IP> <PORT>")
        sys.exit(1)

    ip = sys.argv[1]
    port = sys.argv[2]

    try:
        if icmp_probe(ip):
            syn_ack_packet = syn_scan(ip, port)
            if syn_ack_packet:
                syn_ack_packet.show()
            else:
                print(f"No response from {ip}:{port}. Port might be closed or filtered.")
        else:
            print(f"ICMP probe to {ip} failed. Host may be unreachable.")
    except Exception as e:
        print(f"An error occurred: {e}")
