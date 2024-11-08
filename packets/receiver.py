from scapy.all import sniff, Raw
import socket
import pickle
import pandas as pd


# Load the pre-trained model and label encoder
with open('../model/gb_pipeline.pkl', 'rb') as f:
    pipeline_gb,label_encoder = pickle.load(f)

# Callback function for sniffing packets
def packet_callback(packet):
        data = packet.decode()      
        # Convert data to a DataFrame (assuming comma-separated values in a single line of data)
        data_df = pd.DataFrame([data.split(",")], columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
        'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
        'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
        'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
        'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
        'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
        'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
        'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
        'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
    ])
        
        # Use the loaded pipeline to predict the label
        prediction = pipeline_gb.predict(data_df)
            # Decode the prediction to the original label name
        predicted_label = label_encoder.inverse_transform([prediction[0]])
        # Display the result
        print(f"Packet classified as: {predicted_label}")

def start_tcp_receiver():
    # Define server IP and port
    server_ip = '127.0.0.1'
    server_port = 9999

    # Create a TCP server socket to listen on port 9999
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)  # Listen for incoming connections

    print(f"Server listening on {server_ip}:{server_port}... Press Ctrl + C to stop.")
    
    try:
        while True:
            # Accept incoming connections
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")
            
            # Receive and display data from the sender
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received data from TCP connection: {data.decode()}")
                # Classify received data
                packet_callback(data)
            client_socket.close()
    except KeyboardInterrupt:
        print("\nExiting gracefully.")
        server_socket.close()

# Start receiving packets
start_tcp_receiver()
