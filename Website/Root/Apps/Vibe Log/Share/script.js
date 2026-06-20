
// get option element
e['content'] = document.getElementById('content')

let src = `/Apps/Goofy Stuff/Cursed Images/files/${parameters['name']}`

// Set the html of the 'content' element to an embed image
e.content.innerHTML = `<img src="${src}?raw=true">`

e.title.textContent = `My Vibe (${parameters['iso']})`

e.back.textContent = 'Back'
