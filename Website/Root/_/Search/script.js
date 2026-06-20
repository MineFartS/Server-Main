e['options'] = document.getElementById('options')
e['Search'] = document.getElementById('Search')

let lterm = ''

setInterval(() => {

	let term = e.Search.value.toLowerCase()

	if (term != lterm) {

		// Clear all options
		e.options.innerHTML = ''

		fetch('search.json').then(r => r.json()).then(t => {

			for (x in t) {
				
				// Set 'i' to current item
				var i = t[x]

				// Check if item is visible
				if (i.Visible && i.Title.toLowerCase().includes(term)) {
				
					// Insert element with item details
					e.options.insertAdjacentHTML('beforeend', `
						<a 
							class = "option"
							href = "${i.URL}"
						>${i.Title}</a>
					`)
				
				}

			}
			
			// Show message if no results found
			if (e.options.children.length > 0) {
				e.options.insertAdjacentHTML('afterbegin', `<h2>${e.options.children.length} results</h2>`)
			} else {
				e.options.innerHTML = `<h1>No Results for</h1> <br> <h1 style="line-break: anywhere;">${term}</h1>`
			}

		})

		lterm = term

	}

}, 500)