

async function send(url, redirect) {
    document.getElementById('send-btn').disabled = true;
    const content = document.getElementById('html').value;
    const blob = new Blob([content], { type: 'text/plain' });
    const formData = new FormData();
    const input = document.getElementById('filename');
    var name = 'textarea-content.txt'
    if (input) {
        name = `${input.value}.txt`
    }
    formData.append('file', blob, name);
    
    await fetch(url, {
                    method: 'POST',
                    body: formData
                })
    window.location.replace(redirect);
}