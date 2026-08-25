
postSearch(async (term) => {

    let results = []

    let prom = await fetch(`https://www.omdbapi.com/?apikey=97f79170&s=${term}`);
    let resp = await prom.json();

    if (resp.Response == 'True') {

        for (let i of resp.Search) {

            // Parse the media release year
            i.Year = i.Year.substring(0,4)

            results.push(new ImageResult(
                img = i.Poster,
                callback = () => getItem(i.Type, i.Title, i.Year),
                hover = `${i.Title} (${i.Year})`,
                ig_err = true
            ))
            
        }

    }

    return results

})


function getItem(Type, Title, Year) {

    // Save the current html of the search results
   window.oldNodes = Array.from(e.options.childNodes);

    e.Search.setAttribute('readonly', 'true')

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

    // Clear the loading Dots
    e.options.innerHTML = ''
    
    // Restore the saved search results html
    if (window.oldNodes) {
        for (let node of window.oldNodes) {
            e.options.appendChild(node);
        }
    }

    // Allow the search box to be modified
    e.search.removeAttribute('readonly')

}


