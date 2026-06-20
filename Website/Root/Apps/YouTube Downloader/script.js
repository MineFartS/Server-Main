
e['format'] = document.getElementsByName('format')[0]
e['url']    = document.getElementsByName('url')[0]
e['submit'] = document.getElementById('submit')
e['form']   = document.getElementById('form')

// Regex to extract id from youtube url
let YT_ID_re = /(?:youtube(?:-nocookie)?\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;

function download(event) {

	// prevent page from changing after javascript finishes
	event.preventDefault()

	// Match the given url to the regex
	let match = e.url.value.match(YT_ID_re)

	// If a video ID was found
	if (match) {

		// Get the formatted URL of youtube video
		let id, format;

        id = match[1]
		format = e.format.value

		// Remove the 'form' element
		e.form.remove()

		// Insert loading dots
		document.body.insertAdjacentHTML('beforeend', `
			<div class="loader">
				<span></span>
				<span></span>
				<span></span>
				<span></span>
				<span></span>
				<span></span>
			</div>
		`)

		// Get 'loader' element
		e['loader'] = document.getElementsByClassName('loader')[0]

		// Call API
		API.call(`/Apps/YouTube Downloader/${format}`, {'id':id}).then(t => {

			// Remove 'loading' element
			e.loader.remove()

			// Update the back button
			e.back.textContent = 'Back'
			e.back.setAttribute('href', '.')

			// Insert download button
			document.body.insertAdjacentHTML('beforeend', `
				<a
					href = "${API.url}/Apps/YouTube Downloader/file?name=${t}"
					class = "download"
					target = "_blank"
				>Download</a>
			`)

		})

	// If a video ID wasn't found
	} else {

		// Set the color of the 'url' field to 'red'
		e.url.style.backgroundColor = 'red'

		// Wait 1 second
		setTimeout(() => {

			// Set the color of the 'url' field back to 'white'
			e.url.style.backgroundColor = 'white'
		
		}, 1000);

	}

}
