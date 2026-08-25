// =======================================================
// TYPE DEFINITIONS:

/**
 * @typedef {Object.<string, string|number|boolean>} URLParameters
 */

/**
 * @typedef {Object.<string, string|number|boolean>} BrowserCookies
 */

/**
 * @typedef {Object} AuthResponse
 * @property {boolean} Valid - Indicates if the authentication details are valid.
 * @property {string} [Alert] - Optional alert message to be shown to the user.
 */

// =======================================================
// PATH:

/** 
 * Current domain name ('philh.myftp.biz', 'localhost', ...)
 * @type {string} 
 */
const domain = window.location.href.split('://')[1].split('/')[0];

/** 
 * Get protocol ('http', 'https')
 * @type {string} 
 */
const protocol = window.location.href.split('://')[0];

/** 
 * Get path ('/Apps', ...)
 * @type {string} 
 */
const path = decodeURI(window.location.pathname);

/** 
 * Completely decoded URL string
 * @type {string} 
 */
const href = decodeURIComponent(window.location.href);

/**
 * Extracted parent directory pathname.
 * @param {string} [p=path] - The target path string to extract the parent from.
 * @returns {string} The parent directory pathname ending with a trailing slash.
 */
function ParentPathname(p = path) {		
    let path_segs = p.split('/');

    if (p.endsWith('/')) {
        return path_segs.slice(0, -2).join('/') + '/';
    } else {
        return path_segs.slice(0, -1).join('/') + '/';
    }
}

// =======================================================
// ELEMENTS:

/** 
 * Cached DOM elements wrapper
 * @type {Record<string, HTMLElement | null>} 
 */
const e = {
    'back': document.getElementById('back'),
    'title': document.getElementById('title')
};

// Set title box to the document's title
if (e.title) {
    e.title.textContent = document.title;
}

// Check if not under dir '/_/'
if (!path.startsWith('/_/')) {
    // Set back button text to parent's pathname
    if (e.back) {
        e.back.textContent = ParentPathname(path);
    }
}

// =======================================================
// API

/**
 * Core API utility interface
 */
const API = {

    /** @type {string} */
    'url': `${protocol}://${domain}:8000`,

    /**
     * Executes a native fetch pipeline towards the targeted API pathing endpoint.
     * @param {string} url - API path extension.
     * @param {Object.<string, *>} [params={}] - Key-Value pair options processed as explicit query configurations.
     * @param {number} [timeout] - Maximum allowed lifetime boundary execution limit tracked in seconds.
     * @returns {Promise<*>} Evaluated programmatic server JSON response.
     */
    'call': (
        url,
        params = {},
        timeout = undefined
    ) => {

        /** @type {[string, RequestInit]} */
        let args = [
            API.url + url,
            {
                cache: 'no-store'
            }
        ];

        if (Object.keys(params).length > 0) {
            args[0] += '?';
            args[0] += new URLSearchParams(params).toString();
        }

        if (timeout) {
            args[1]['signal'] = AbortSignal.timeout(timeout * 1000);
        }

        // Return a promise object with json formatting
        return fetch(...args).then(r => r.json());

    },

    /**
     * Authenticated endpoint execution mechanism.
     * @param {string} url - API path extension.
     * @param {Object.<string, *>} [params={}] - Key-Value pair options processed as explicit query configurations.
     * @param {number} [timeout] - Maximum allowed lifetime boundary execution limit tracked in seconds.
     * @returns {Promise<AuthResponse>} Evaluated programmatic server JSON payload validation state wrapper.
     */
    'auth': (
        url,
        params = {},
        timeout = undefined
    ) => {

        // Add Username to the params
        params['username'] = cookies['username'];

        // Add Token to the params
        params['token'] = cookies['token'];

        // Return API.call function with updated params
        return API.call(url, params, timeout);

    }

};

// =======================================================
// PARAMETERS:

/** 
 * Parsed parameters mapped dynamically out of active browser contexts.
 * @type {URLParameters} 
 */
const parameters = {};

// Check if any params are in the url
if (window.location.href.includes('?')) {

    // Get unformatted param list
    let rparams = window.location.search.substring(1).split('&');

    // Iter through raw params
    for (let x in rparams) {

        // Separate the key and value 
        let [key, value] = rparams[x].split('=');

        /** @type {string | boolean | number} */
        let parsedValue = value;

        // Check if value is bool, then format
        if (['true', 'false'].includes(value)) {
            parsedValue = (value == 'true');
        }

        // Check if value is Number, then format
        if (!isNaN(Number(value))) {
            parsedValue = Number(value);
        }
        
        // Save decoded Value to key in params dict
        parameters[key] = typeof parsedValue === 'string' ? decodeURIComponent(parsedValue) : parsedValue;

    }

}

// =======================================================
// COOKIES:

/** 
 * Parsed cookie collection storage element.
 * @type {BrowserCookies} 
 */
const cookies = {};

// Get unformatted cookies list
var rcookies = document.cookie.split('; ');

// Iter through raw cookies
for (let x in rcookies) {

    // Separate the key and value
    let [key, value] = rcookies[x].split('=');

    /** @type {string | boolean | number} */
    let parsedValue = value;

    // Check if value is bool, then format
    if (['true', 'false'].includes(value)) {
        parsedValue = (value == 'true');
    }

    // Check if value is Number, then format
    if (!isNaN(Number(value))) {
        parsedValue = Number(value);
    }
    
    cookies[key] = parsedValue;
}

// =======================================================
// AUTHENTICATION:

/**
 * Validates the user's active session permissions against the verification server.
 * @returns {void}
 */
function authorize() {

    // Contact server with authentication details and read response
    API.auth('/login/auth').then(t => {

        if (t.Alert) {
            alert(t.Alert);
        }

        // If authentication details are invalid
        if (!t.Valid) {

            // Redirect User to the login page
            window.location.href = `/_/Account/Login?dest=${path}`;

        }

    });

}

// =======================================================

/** 
 * Auto-evaluated operating system identity.
 * @type {'MacOS' | 'Windows' | 'Linux' | undefined} 
 */
const OS = (() => {
  
    /** @type {string} */
    let platform = (
        /** @type {*} */(window.navigator)?.userAgentData?.platform || 
        window.navigator.platform
    );
  
    if (['macOS', 'Macintosh', 'MacIntel'].includes(platform)) return 'MacOS';

    if (['Win32', 'Win64', 'Windows'].includes(platform)) return 'Windows';

    if (/Linux/.test(platform)) return 'Linux';

    return undefined;

})();

// =======================================================

