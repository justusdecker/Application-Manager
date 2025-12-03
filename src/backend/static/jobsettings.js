
const inputs = document.querySelectorAll('.tag-input');

async function load() {

    var data = []
    const response = await fetch('/jobsearch_settings_as_json', {
        method: 'GET',
        headers: {
            'Accept': 'text/plain'
        }
    }
    )
    const text = await response.text()
    text.split(';').forEach(tagList => {
            var tags = [];
            tagList.split(',').forEach(tag => {
                tags.push(tag);
            })
            data.push(tags)
        })
    return data
}




async function send() {
    // Will send the data to the internal server.
    var contents = [];
    inputs.forEach(input =>{
        contents.push(input.tags);
    });
    console.log(contents);
    const blob = new Blob([JSON.stringify(contents, null, 2)], {type: 'application/json'});
    const formData = new FormData();
    formData.append('file', blob, 'test.txt')
}

// AI-generated
document.addEventListener('DOMContentLoaded', () => {
    load().then(all_data => {
    console.log(all_data)

        var i = 0;
        inputs.forEach(input => {
            var data = all_data[i]
            input.tags = data;
            data.forEach(tag => {
                console.log(tag);
                addTagManually(tag, input);
            })
            i++;
            input.addEventListener('keyup', addTag);
    });
    })
    

    function createTags(inputElement) {
        const canvas = inputElement.closest('.tag-canvas');

        const tagList = canvas.querySelector('.tag-list');

        tagList.querySelectorAll('li').forEach(li => li.remove());

        inputElement.tags.slice().reverse().forEach(tag => {
            let liTag = document.createElement('li');
            liTag.innerText = tag;
            
            liTag.className = 'tag-entry'; 

            liTag.addEventListener('click', () => {
                remove(inputElement, tag);
            });

            tagList.appendChild(liTag);
        });
    }

    function remove(inputElement, tag) {
        let index = inputElement.tags.indexOf(tag);
        if (index > -1) {
            
            inputElement.tags = [
                ...inputElement.tags.slice(0, index), 
                ...inputElement.tags.slice(index + 1)
            ];
            
            createTags(inputElement);
        }
    }

    function addTag(e) {
        let inputElement = e.target;
        let val = inputElement.value.replace(/\s+/g, ' ').trim();

        if (e.key === "Enter") {
            if (val.length > 1) {
                val.split(',').forEach(tag => {
                    let cleanTag = tag.trim().toLowerCase();
                    
                    if (cleanTag.length > 0 && !inputElement.tags.includes(cleanTag)) {
                        inputElement.tags.push(cleanTag);
                    }
                });
                
                createTags(inputElement);
                inputElement.value = '';
            }
        }
    }

    function addTagManually(text, inputE) {
        let inputElement = text;
        let val = inputElement.replace(/\s+/g, ' ').trim();

        
        if (val.length > 1) {
            val.split(',').forEach(tag => {
                let cleanTag = tag.trim().toLowerCase();
                
                if (cleanTag.length > 0 && !inputElement.includes(cleanTag)) {
                    inputElement.tags.push(cleanTag);
                }
            });
            
            createTags(inputE);
        }
        
    }
});