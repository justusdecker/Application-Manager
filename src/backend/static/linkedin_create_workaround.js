async function send() {
    document.getElementById('send-btn').disabled = true;
    const content = document.getElementById('html').value;
    const blob = new Blob([content], { type: 'text/plain' });
    const formData = new FormData();
    formData.append('file', blob, 'textarea-content.txt');
    window.location.replace("/load");
    await fetch('/linkedin/create', {
                    method: 'POST',
                    body: formData
                }).then(e =>{
                    console.log("test");
                    window.location.replace("/linkedin");
                }).catch(e => {
                    console.log(e);
                })
    
}
