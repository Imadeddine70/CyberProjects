from flask import Flask, request, jsonify
from flask_cors import CORS
import nmap
import concurrent.futures
import logging

app = Flask(__name__)
CORS(app)  # Permet de gérer les requêtes Cross-Origin

logging.basicConfig(level=logging.DEBUG)

# Fonction pour scanner un hôte
def scan_host(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, '1-1000')
    result = ""
    if target in scanner.all_hosts():
        for protocol in scanner[target].all_protocols():
            result += f"Protocol: {protocol}\n"
            ports = scanner[target][protocol].keys()
            for port in ports:
                state = scanner[target][protocol][port]['state']
                service = scanner[target][protocol][port]['name']
                result += f"Port {port}: {state}, service: {service}\n"
    else:
        result = "No results for this target."
    
    return {'target': target, 'result': result}

# Route pour le scan réseau
@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    targets = data.get('targets')

    logging.debug(f'Received targets: {targets}')  # Log the received targets

    if not targets or not isinstance(targets, list) or all(not target for target in targets):
        return jsonify({'error': 'No valid targets provided.'}), 400

    results = {}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_target = {executor.submit(scan_host, target): target for target in targets if target}
        for future in concurrent.futures.as_completed(future_to_target):
            target = future_to_target[future]
            try:
                results[target] = future.result()
            except Exception as exc:
                results[target] = {'target': target, 'result': str(exc)}

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
