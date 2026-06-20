
e['username'] = document.getElementById('username')
e['password'] = document.getElementById('password')

// Destination URL
let dest = parameters['dest']

// Back URL
let back = ParentPathname(dest)

const APIwrapper = class {

    constructor(url) {
        this.url = `/login/${url}/`
    }

    run(params={}) {

        params['username'] = e.username.value;
        params['password'] = e.password.value;
            
        let conn = API.call(this.url, params)

        conn.then(t => {
            
            if (t.Alert) {
                alert(t.Alert)
            }

            if (t.Valid) {

                document.cookie = `username=${e.username.value}; path=/`

                document.cookie = `token=${t.Token}; path=/`

                window.location.href = dest

            }

        })

    }

}
