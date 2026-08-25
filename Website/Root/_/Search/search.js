/**
 * @callback SearchCallback
 * @param {string} term
 * @returns {Result[]}
 */

e['Search'] = document.getElementById('Search')

class Result {
    
    /**
     * @param {string} title 
     * @param {string} url 
     */
    constructor(title, url) {

        /** @type {string} */
        this.title = title

        /** @type {string} */
        this.url = url

    }

}

/**
 * @param {SearchCallback} callback 
 */
function postSearch(callback) {

    let lterm = ''

    setInterval(() => {

        let term = e.Search.value.toLowerCase()

        if (term != lterm) {

            let results = callback(term);

            // Clear all options
            e.options.innerHTML = ''

            for (let r of results) {
                e.options.insertAdjacentHTML('beforeend', `
                    <a class="option" href="${r.url}">${r.title}</a>
                `)
            } 

            lterm = term;

            // Show message if no results found
            if (e.options.children.length > 0) {
                e.options.insertAdjacentHTML('afterbegin', `<h2>${e.options.children.length} results</h2>`)
            } else {
                e.options.innerHTML = `<h1>No Results for</h1> <br> <h1 style="line-break: anywhere;">${term}</h1>`
            }

        }

    }, 500)
}

