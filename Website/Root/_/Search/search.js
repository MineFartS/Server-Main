/**
 * @callback SearchCallback
 * @param {string} term
 * @returns {Result[]}
 */

/**
 * @callback ClickCallback
 * @param {PointerEvent} event
 * @returns {void}
 */

e['Search'] = document.getElementById('Search')
e['options'] = document.getElementById('options')

class Result {
    
    /**
     * @param {string|ClickCallback} callback Can be a URL string or a function
     * @param {string} tag
     */
    constructor(callback, tag) {

        /** @type {string} */
        this.tag = tag

        /** @type {string} */
        this.callback = callback

    }

    /**
     * @returns {HTMLElement}
     */
    build() {

        let e = document.createElement(this.tag);
        
        if (typeof this.callback === 'string') {
            e.setAttribute('href', this.callback)
        } else {
            e.addEventListener('click', evt=>{
                evt.preventDefault();
                this.callback(evt);
            });
        }

        return e
    }

}

class TextResult extends Result {

    /**
     * @param {string} title 
     * @param {string|ClickCallback} callback Can be a URL string or a function
     */
    constructor(title, callback) {
        super(callback, 'a')

        /** @type {string} */
        this.title = title
    
    }

    /**
     * @returns {HTMLElement}
     */
    build() {
        let e = super.build()
        e.setAttribute('class', 'option')
        e.textContent = this.title
        return e
    }

}

class ImageResult extends Result {

    /**
     * @param {string} img Image URL
     * @param {string|ClickCallback} callback Can be a URL string or a function
     * @param {string} hover Hover Text
     * @param {boolean} ig_err Ignore Images with Loading Errors
     */
    constructor(img, callback, hover='', ig_err=false) {
        super(callback, 'img')

        /** @type {string} */
        this.img = img

        /** @type {string} */
        this.hover = hover

        /** @type {boolean} */
        this.ig_err = ig_err
    
    }

    /**
     * @returns {HTMLElement}
     */
    build() {
        let e = super.build()
        
        e.setAttribute('src', this.img);
        e.setAttribute('title', this.hover);

        if (this.ig_err) {
            e.setAttribute('onerror', "this.remove()");
        }

        return e
    }

}

/**
 * @param {SearchCallback} callback 
 */
function postSearch(callback) {

    const results = {};

    let lterm = ''

    setInterval(async () => {

        let term = e.Search.value.toLowerCase().trim()

        if (term != lterm) {
            
            lterm = term;

            if (results[term] == undefined) {
                results[term] = await callback(term);
            }

            // Clear all options
            e.options.innerHTML = ''

            for (let r of results[term]) {
                e.options.insertAdjacentElement('beforeend', r.build())
            } 

            // Show message if no results found
            if (e.options.children.length > 0) {
                e.options.insertAdjacentHTML('afterbegin', `<h2>${e.options.children.length} results</h2>`)
            } else {
                e.options.innerHTML = `<h1>No Results for</h1> <br> <h1 style="line-break: anywhere;">${term}</h1>`
            }

        }

    }, 500)
}

