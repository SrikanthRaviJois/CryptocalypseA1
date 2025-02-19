import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(f"\nPeer: {message}")
        except:
            print("Connection closed.")
            sock.close()
            break

def send_messages(sock):
    try:
        while True:
            message = input("Enter message (or type 'exit' to quit chat): ")
            if message.lower() == 'exit':
                print("Exiting chat...")
                break
            sock.sendall(message.encode())
    except (EOFError, OSError):
        print("Input stream closed or unavailable. Exiting...")

def list_peers(connected_peers):
    if connected_peers:
        print("\nConnected Peers:")
        for idx, peer in enumerate(connected_peers, start=1):
            print(f"{idx}. {peer}")
    else:
        print("\nNo connected peers.")

def get_user_choice(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, OSError):
        print("Input stream closed or unavailable. Exiting...")
        return "3"  # Default to exit if input fails

def start_p2p_chat():
    user_name = input("Enter your name: ").strip()
    port = int(input("Enter port number to listen on: ").strip())
    
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.bind(("0.0.0.0", port))  # Bind to user-specified port
    peer_socket.listen(5)
    print(f"{user_name} is waiting for a connection on port {port}...")
    
    connected_peers = []
    threading.Thread(target=accept_connections, args=(peer_socket, connected_peers)).start()
    
    while True:
        print("\nOptions:")
        print("1. Send a message")
        print("2. Query connected peers")
        print("3. Quit")
        choice = get_user_choice("Select an option: ")
        
        if choice == "1":
            peer_ip = get_user_choice("Enter peer IP to message: ")
            peer_port = int(get_user_choice("Enter peer port number: "))
            try:
                peer_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_conn.connect((peer_ip, peer_port))
                print("Connected to peer.")
                connected_peers.append(f"{peer_ip}:{peer_port}")
                threading.Thread(target=receive_messages, args=(peer_conn,)).start()
                send_messages(peer_conn)
            except Exception as e:
                print(f"Connection failed: {e}")
        elif choice == "2":
            list_peers(connected_peers)
        elif choice == "3":
            print("Exiting chat application.")
            break
        else:
            print("Invalid option. Please try again.")

def accept_connections(server_socket, connected_peers):
    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        connected_peers.append(f"{addr[0]}:{addr[1]}")
        threading.Thread(target=receive_messages, args=(conn,)).start()
        send_messages(conn)

if __name__ == "__main__":
    start_p2p_chat()
