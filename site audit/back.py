from flask import Flask, request, jsonify
from flask_cors import CORS
import nmap

app = Flask(__name__)
CORS(app)  # Permet de gérer les requêtes Cross-Origin

# Étape 1 : Scanner le réseau pour trouver les ports ouverts et les services
def scan_network(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, '1-1000')
    return scanner

# Route de test pour vérifier si le serveur fonctionne
@app.route('/')
def index():
    return "Server is running!"

# Route pour le scan réseau
@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    target = data.get('target')
    
    # Étape 1 : Scan de Réseau
    network_results = scan_network(target)
    
    # Générer un rapport simple pour l'affichage
    result = ""
    if target in network_results.all_hosts():
        for protocol in network_results[target].all_protocols():
            result += f"Protocol: {protocol}\n"
            ports = network_results[target][protocol].keys()
            for port in ports:
                state = network_results[target][protocol][port]['state']
                service = network_results[target][protocol][port]['name']
                result += f"Port {port}: {state}, service: {service}\n"
    else:
        result = "No results for this target."
    
    return jsonify({'target': target, 'result': result})

if __name__ == "__main__":
    app.run(debug=True)
