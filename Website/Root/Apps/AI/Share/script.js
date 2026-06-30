fetch(`responses/${data.Param.get('id')}.json`).then(r => r.json()).then(t => {
    document.getElementById('prompt').value = t.prompt
    document.getElementById('response').innerHTML = t.response
    var created = new Date(t.created * 1000)

    document.getElementById('1').innerHTML += t.username
    document.getElementById('2').innerHTML += t.model
    document.getElementById('3').innerHTML += `${created.toLocaleDateString()} at ${created.toLocaleTimeString()}`
})