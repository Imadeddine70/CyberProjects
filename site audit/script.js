document.getElementById('scanner-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const targetIps = document.getElementById('target-ip').value.split(',').map(ip => ip.trim()).filter(ip => ip); // Filter out empty inputs

    if (targetIps.length === 0) {
        alert("Please enter at least one valid target IP address.");
        return; // Exit if no valid IPs are provided
    }

    // Show loading indicator
    document.getElementById('loading').style.display = 'block';
    document.getElementById('output').style.display = 'none'; // Hide output until results are ready

    const response = await fetch('http://127.0.0.1:5000/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ targets: targetIps }) // Send the list of targets
    });

    const data = await response.json();

    // Hide loading indicator
    document.getElementById('loading').style.display = 'none';

    if (response.ok) {
        displayResults(data);
    } else {
        alert(`Error: ${data.error || 'An unknown error occurred.'}`);
    }
});

function displayResults(data) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = ''; // Reset previous content

    for (const key in data) {
        const result = data[key];
        outputDiv.innerHTML += `<h2>Scan Results for ${result.target}</h2><pre>${result.result}</pre>`;
    }

    outputDiv.style.display = 'block'; // Show output after results are ready
}
