
// get option element
e['options'] = document.getElementById('options')

// Fetch 'index.json'
fetch('index.json').then(r => r.json()).then(t => {

	for (x in t) {
		
		// Set 'i' to current item
		var i = t[x]

		// Check if item is visible
		if (i.Visible) {

			// Insert element with item details
			e.options.insertAdjacentHTML('beforeend', `
				<a 
					class = "option"
					href = "${i.URL}"
				>${i.Title}</a>
			`)
		}
	}
})

// check if in root page
if (window.location.pathname == '/') {
	// remove back button
	e.back.setAttribute('href', '/_/Search')
	e.back.textContent = 'Search'
}