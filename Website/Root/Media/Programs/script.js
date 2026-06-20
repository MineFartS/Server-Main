// get option element
e['options'] = document.getElementById('options')

// Fetch 'index.json'
API.call('/Media/Programs/list', {'os': OS}).then(t => {

	for (let name of t) {

        // Insert element with item details
        e.options.insertAdjacentHTML('beforeend', `
            <a 
                class = "option"
                href = "${API.url}/Media/Programs/get?os=${OS}&name=${name}"
            >${name.replaceAll('_', ' ').trim()}</a>
        `)
		
	}

})