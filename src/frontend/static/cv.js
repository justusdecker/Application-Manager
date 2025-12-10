
async function write_improve() {
    const improve_writing_textarea = document.getElementById('imp_writing');
    const summary_textarea = document.getElementById('summary');

    const formData = new FormData();
    formData.append('text', improve_writing_textarea.value);

    await fetch("/aiiw", {
                    method: 'POST',
                    body: formData
                }).then(response => {
                    response.json().then(data => {
                    console.log(data);
                    summary_textarea.value = data['text'];

                    })
                })
}