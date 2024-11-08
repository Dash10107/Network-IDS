from scapy.all import IP, TCP, Raw, send
import socket

# Sample data to send
sample_data = [
    "0,tcp,telnet,S0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,120,120,1.00,1.00,0.00,0.00,1.00,0.00,0.00,235,171,0.73,0.07,0.00,0.00,0.69,0.95,0.02,0.00",
    "0,tcp,http,SF,213,659,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,24,24,0.00,0.00,0.00,0.00,1.00,0.00,0.00,255,255,1.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00",
    "0,tcp,http,SF,246,2090,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,16,16,0.00,0.00,0.00,0.00,1.00,0.00,0.00,35,255,1.00,0.00,0.03,0.05,0.00,0.00,0.00,0.00",
    "0,udp,private,SF,45,44,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,505,505,0.00,0.00,0.00,0.00,1.00,0.00,0.00,255,255,1.00,0.00,1.00,0.00,0.00,0.00,0.00,0.00"
    ]

def send_packets(data):
    # Define server IP and port
    server_ip = '127.0.0.1'
    server_port = 9999

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the receiver
        client_socket.connect((server_ip, server_port))

        # Send each packet (entry from data)
        for entry in data:
            # Send the entry as a TCP packet
            packet = IP(dst=server_ip) / TCP(dport=server_port) / Raw(load=entry.encode())
            print(f"Sending packet: {entry}")
            send(packet)  # Send the packet using Scapy
            client_socket.send(entry.encode())  # Send it via TCP (for reliable delivery)

    finally:
        # Close the socket after sending all data
        client_socket.close()

# Start sending packets
send_packets(sample_data)
