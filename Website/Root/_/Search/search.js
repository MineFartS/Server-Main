/**
 * @callback SearchCallback
 * @param {string} term
 * @returns {Result[]}
 */

e['Search'] = document.getElementById('Search')

/**
 * @callback ClickCallback
 * @param {PointerEvent} event
 * @returns {void}
 */

class Result {
    
    /**
     * @param {string|ClickCallback} callback Can be a URL string or a function
     */
    constructor(title, callback) {

        /** @type {string} */
        this.callback = callback

        /** @type {boolean} */
        this.isUrl = (typeof callback === 'string');

    }

    /**
     * @returns {HTMLElement}
     */
    build() {
        return null;
    }

}

class TextResult extends Result {

    /**
     * @param {string} title 
     * @param {string|ClickCallback} callback Can be a URL string or a function
     */
    constructor(title, callback) {
        super(callback)

        /** @type {string} */
        this.title = title
    
    }

    /**
     * @returns {HTMLElement}
     */
    build() {

        let e = document.createElement('a')
        e.setAttribute('class', 'option')
        e.textContent = this.title
        
        if (this.isUrl) {
            e.setAttribute('href', this.callback)
        } else {
            e.setAttribute('href', '#')
            e.addEventListener('click', this.callback)
        }

        return e
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
                e.options.insertAdjacentElement('beforeend', r.build())
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

