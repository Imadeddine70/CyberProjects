import nmap

# Étape 1 : Scanner le réseau pour trouver les ports ouverts et les services
def scan_network(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, '1-1000')
    return scanner

# Étape 2 : Analyser les vulnérabilités connues sur les ports ouverts
def scan_vulnerabilities(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, arguments='--script vuln')
    return scanner

# Étape 3 : Générer un rapport de sécurité
def generate_report(target, scan_results):
    report_file = f"{target}_security_report.txt"
    with open(report_file, 'w') as f:
        f.write(f"--- Security Report for {target} ---\n\n")
        
        for protocol in scan_results[target].all_protocols():
            f.write(f"Protocol: {protocol}\n")
            ports = scan_results[target][protocol].keys()
            for port in ports:
                state = scan_results[target][protocol][port]['state']
                service = scan_results[target][protocol][port]['name']
                f.write(f"Port {port}: {state}, service: {service}\n")
    
    print(f"Security report saved as {report_file}")

# Exécution principale
if __name__ == "__main__":
    target_ip = input("Enter the target IP: ")
    
    # Étape 1 : Scan de Réseau
    print("Starting network scan...")
    network_results = scan_network(target_ip)
    
    # Étape 2 : Analyse des Vulnérabilités
    print("Starting vulnerability scan...")
    vulnerability_results = scan_vulnerabilities(target_ip)
    
    # Étape 3 : Génération du Rapport
    generate_report(target_ip, network_results)
