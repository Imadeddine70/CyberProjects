import socket
import threading
from datetime import datetime

# Liste pour stocker les ports ouverts
open_ports = []

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open")
            open_ports.append(port)  # Ajouter le port ouvert à la liste
        s.close()
    except:
        pass

def start_scan(ip, start_port, end_port):
    print(f"Scanning {ip} from port {start_port} to {end_port}")
    start_time = datetime.now()
    
    threads = []
    
    # Scanner chaque port dans la plage
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = datetime.now()
    scan_duration = end_time - start_time

    # Informations supplémentaires
    total_ports_scanned = end_port - start_port + 1
    open_ports_count = len(open_ports)
    
    # Résumé du scan
    print("\n--- Scan Summary ---")
    print(f"Total ports scanned: {total_ports_scanned}")
    print(f"Open ports found: {open_ports_count}")
    if open_ports:
        print(f"List of open ports: {open_ports}")
    else:
        print("No open ports found.")
    print(f"Scan completed in: {scan_duration}")

if __name__ == "__main__":
    target_ip = input("Enter the target IP: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))
    
    start_scan(target_ip, start_port, end_port)
