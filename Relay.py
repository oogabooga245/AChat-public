import socket
import threading

clients = []
relays = []

def handle_connection(conn, is_relay=False):
    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break
            for client in clients:
                if client != conn:
                    try:
                        client.sendall(message)
                    except:
                        clients.remove(client)
            for relay in relays:
                if relay != conn:
                    try:
                        relay.sendall(message)
                    except:
                        relays.remove(relay)
        except:
            break
    if is_relay:
        relays.remove(conn)
    else:
        clients.remove(conn)
    conn.close()

def accept_clients(server_socket):
    while True:
        client_conn, client_addr = server_socket.accept()
        clients.append(client_conn)
        threading.Thread(target=handle_connection, args=(client_conn, False)).start()

def connect_to_relay(relay_host, relay_port):
    try:
        relay_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        relay_conn.connect((relay_host, relay_port))
        relays.append(relay_conn)
        threading.Thread(target=handle_connection, args=(relay_conn, True)).start()
        print(f"Connected to relay: {relay_host}:{relay_port}")
    except Exception as e:
        print(f"Failed to connect to relay {relay_host}:{relay_port}: {e}")

def start_relay_server(host, port, parent_host, parent_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"AChat Relay running on {host}:{port}")
    threading.Thread(target=accept_clients, args=(server_socket,)).start()
    connect_to_relay(parent_host, parent_port)

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 9000
    PARENT_HOST = "69.164.196.248"
    PARENT_PORT = 9000
    start_relay_server(HOST, PORT, PARENT_HOST, PARENT_PORT)
