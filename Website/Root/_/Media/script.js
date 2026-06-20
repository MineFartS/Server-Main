	
e['content'] = document.getElementById('content')

fetch('/_/Media/MimeTable.json').then(r => r.json()).then(MimeTable => {

    //============================================================================================

    window.media = {}

    let URL = decodeURIComponent(document.location.pathname)
    
    media['url'] = URL + '?raw=true'

    media['back'] = URL.substring(0, URL.lastIndexOf('/')+1)

    media['name'] = URL.substring(URL.lastIndexOf('/')+1)

    media['ext'] = URL.substring(URL.lastIndexOf('.')+1).toLowerCase()

    media['mime'] = MimeTable[media.ext]

    media['type'] = media.mime.split('/')[0]

    //============================================================================================

    e.back.textContent = media.back
    e.back.setAttribute('href', media.back)

    document.title = media.name
    e.title.textContent = media.name.substring(0, media.name.lastIndexOf('.'))

    //============================================================================================

    e.content.setAttribute('src', media.url)
	e.content.setAttribute('type', media.mime)

    //============================================================================================

	if (media.type == 'audio') {
		e.content.setAttribute('style', 'height: auto')
	}

})
