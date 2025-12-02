
document.addEventListener('DOMContentLoaded', () => {

    const inputs = document.querySelectorAll('.tag-input');

    inputs.forEach(input => {
        input.tags = [];
        input.addEventListener('keyup', addTag);
    });

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
});