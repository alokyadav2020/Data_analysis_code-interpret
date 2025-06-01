document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    const chartType = document.getElementById('chartType').value;
    formData.append('chartType', chartType);
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<div id="status-step">1. File uploaded...<br></div>';
    try {
        resultDiv.innerHTML += '<div id="status-step">2. Processing file...<br></div>';
        const response = await fetch('/uploadfile/', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        // Dynamically update status steps from backend
        if (data.status_steps && Array.isArray(data.status_steps)) {
            resultDiv.innerHTML = data.status_steps.map(s => `<div id='status-step'>${s}</div>`).join('');
        }
        if (response.ok) {
            let chartHtml = data.chart_html ? `<div id='chart-container'>${data.chart_html}</div>` : '';
            let tableHtml = data.table_html || '';
            let codeHtml = data.generated_code ? `<pre class='code-block'>${data.generated_code}</pre>` : '';
            resultDiv.innerHTML += data.message + ' (' + data.filename + ')<br><br>' + tableHtml + chartHtml + codeHtml;
        } else {
            resultDiv.textContent = data.detail || 'Upload failed.';
        }
    } catch (err) {
        resultDiv.textContent = 'Error uploading file.';
    }
});
