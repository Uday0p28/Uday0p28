from scapy.all import sniff, IP, TCP, UDP, Raw, DNS, DNSQR, DNSRR

def analyze_packet(packet):
    print("\n=== New Packet Captured ===")

    # Check if packet has IP layer
    if IP in packet:
        ip_layer = packet[IP]
        print(f"Source IP: {ip_layer.src}")
        print(f"Destination IP: {ip_layer.dst}")
        print(f"Protocol Number: {ip_layer.proto}")

    # Check for TCP packets
    if TCP in packet:
        tcp_layer = packet[TCP]
        print(f"--- TCP Layer ---")
        print(f"Source Port: {tcp_layer.sport}")
        print(f"Destination Port: {tcp_layer.dport}")
        print(f"Flags: {tcp_layer.flags}")

        # Check for HTTP traffic (port 80 or 443)
        if tcp_layer.dport in [80, 443] or tcp_layer.sport in [80, 443]:
            print("Likely HTTP/HTTPS traffic")

    # Check for UDP packets
    if UDP in packet:
        udp_layer = packet[UDP]
        print(f"--- UDP Layer ---")
        print(f"Source Port: {udp_layer.sport}")
        print(f"Destination Port: {udp_layer.dport}")

        # Check for DNS traffic (port 53)
        if udp_layer.dport == 53 or udp_layer.sport == 53:
            print("Likely DNS traffic")
            if DNS in packet:
                dns = packet[DNS]
                if dns.qr == 0:  # query
                    print(f"DNS Query for: {dns[DNSQR].qname.decode()}")
                elif dns.qr == 1:  # response
                    print(f"DNS Response: {dns[DNSRR].rdata}")

    # Extract raw payload if available
    if Raw in packet:
        raw_data = packet[Raw].load
        print(f"--- Raw Payload ---")
        try:
            print(raw_data.decode(errors="ignore")[:100])  # print first 100 chars
        except:
            print(raw_data[:100])  # fallback to raw bytes

# Start sniffing (requires root/admin privileges)
print("Starting packet capture... Press Ctrl+C to stop.")
sniff(prn=analyze_packet, count=0)  # count=0 means infinite capture