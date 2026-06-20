
function getItem(Type, Title, Year) {

    // Save the current html of the search results
    window.oldHTML = e.options.innerHTML

    e.search.setAttribute('readonly', 'true')

    // Add loading dots
	e.options.innerHTML = `
		<div class="loader">
			<span></span>
			<span></span>
			<span></span>
			<span></span>
			<span></span>
			<span></span>
		</div>
	`

    // Parse the media title
    Title = Title
        .replace('&', 'and')
        .replace(':', '')

    // Call the API
    let call = API.call(

        url = '/Server/Plex/download',

        params = {
            'Type': Type,
            'Title': Title,
            'Year': Year
        }
        
    )

    // Handle a Failed API response
    call.catch(responseHandler)

    // Handle a Successful API response
    call.then(responseHandler)

}

function responseHandler(t) {
    
    // Show an alert with the response message
    alert(t)

    // Restore the saved search results html
    e.options.innerHTML = oldHTML

    // Allow the search box to be modified
    e.search.removeAttribute('readonly')

}

