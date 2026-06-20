
authorize()

e['switch'] = document.getElementsByClassName('switch')[0]
e['checkbox'] = e.switch.children[0]

API.url += '/Server/Virtual Machines/'

API.auth('status').then(s => {e.checkbox.checked = s})

function connect() {

    window.location.href = `${API.url}connectRDP?username=${cookies.username}&token=${cookies.token}`

}

function update() {

    API.auth(e.checkbox.checked ? 'start' : 'stop')

}
