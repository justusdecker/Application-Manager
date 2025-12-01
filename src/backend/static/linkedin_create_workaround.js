async function send() {
    const content = document.getElementById('html').value;
    const blob = new Blob([content], { type: 'text/plain' });
    const formData = new FormData();
    formData.append('file', blob, 'textarea-content.txt');
    const response = await fetch('/linkedin/create', {
                    method: 'POST',
                    body: formData
                });
}
