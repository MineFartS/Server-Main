
// get option element
e['content'] = document.getElementById('content')

// Get the content type by reading 'type.ini'
fetch('type.ini').then(r => r.text()).then(t => {

    // Save 't' to global variable 'type'
    window.type = t.trim()

    // If content type is 'text'
    if (type == 'text') {

        // Fetch 'lines.json'
        fetch('lines.json').then(r => r.json()).then(l => {
            
            // Set global 'lines' to 'l'
            window.lines = l

            // Execute 'run' Function
            run()

        })

    // If content type is 'image' or 'video
    } else if (['image', 'video'].includes(type)) {

        // Fetch 'files/index.json'
        fetch('files/index.json').then(r => r.json()).then(items => {
            
            // Create new global array
            window.lines = []

            // Iter through items
			for (x in items) {
				
				// Set 'i' to current item
				var i = items[x]

				// Check if item is visible
				if (i.Visible) {

                    // Append the item to the 'lines' array
                    lines.push(i.URL + '?raw=true')

                }

            }

            // Execute 'run' Function
            run()

        })

    }

})

function run() {

    // If all lines have been shown
    if (lines.length == 0) {

        // Show alert to user
        alert("You've seen it all!")

        // Go back
        e.back.click()

    // If there are lines remaining
    } else {

        // Get a random index from 'lines'
        let x = Math.floor(Math.random() * lines.length);

        // Set 'line' to the randomly selected line
        let line = lines[x]

        // If content type is 'text'
        if (type == 'text') {

            // Set the html of the 'content' element to the first part of the line
            e.content.innerHTML = line[0]

            // If line has a second part
            if (line[1]) {

                // Append a reveal element to the 'content' element
                e.content.innerHTML += `
                    <details>
                        <summary style="font-size: medium">Reveal</summary>
                        ${line[1]}
                    </details>`
            
            }

        // If content type is 'image'
        } else if (type == 'image') {

            // Set the html of the 'content' element to an embed image
            e.content.innerHTML = `<img src="${line}">`

        // If content type is 'video'
        } else if (type == 'video') {

            // Set the html of the 'content' element to an autoplaying embed video
            e.content.innerHTML = `<video autoplay src="${line}">`

        }

        // Remove line from 'lines'
        delete lines[x]

        // Reindex 'lines'
        lines = [...lines].filter((v) => (v != undefined))

    }

}
