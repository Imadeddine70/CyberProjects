document.getElementById('scanner-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const targetIp = document.getElementById('target-ip').value;
    
    const response = await fetch('http://127.0.0.1:5000/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ target: targetIp })
    });
    
    const data = await response.json();
    displayResults(data);
});

function displayResults(data) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = `<h2>Scan Results for ${data.target}</h2><pre>${data.result}</pre>`;
}
