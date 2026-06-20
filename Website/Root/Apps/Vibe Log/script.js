
// get option element
e['content'] = document.getElementById('content2')

e.title.innerHTML += "<br>&#x2022;<br>Click the image that best matches your vibe"

let ISO = new Date().toISOString().substring(0, 10);

// Fetch 'files/index.json'
fetch('/Apps/Goofy Stuff/Cursed Images/files/index.json').then(r => r.json()).then(items => {

    // Remove invisible items
    items.filter(i => i.Visible)

    // Shuffle items
    items.sort(() => Math.random()-0.5)

    let x, src, name;

    for (x=0; x<9; x++) {

        src = items[x].URL;

        name = src.substring(src.lastIndexOf('/')+1);

        // Set the html of the 'content' element to an embed image
        e.content.innerHTML += `
        <a href="Share?name=${name}&iso=${ISO}">
            <img src="${src}?raw=true">    
        </a>`

    }

})
