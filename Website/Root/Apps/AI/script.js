var jsonid = undefined
var model = "smollm2"
var Loaded = 0
var LoadingDotCount = 0

function share() {
    if (jsonid == undefined) {
        alert('Enter a prompt first')
    } else {
        window.top.location.href = 'Share?id='+jsonid
    }
}

function setmodel() {
    const models = [
        ["smollm2", "Quick and lightweight"],
        ["llava", "Vivid Descriptions"],
        ["deepseek-llm", "Advanced Language"],
        ["wizard-math", "Math and Logic"]
    ]
    for (x = 0; x < models.length; x++) {
        if (models[x][0] == model) {
            modelIndex = x
        }
    }
    var message =
        `Enter the number of the model to use

Current Model: ${modelIndex+1} - ${model}\n`
    for (x = 0; x < models.length; x++) {
        message += `\n${x+1} - ${models[x][0]} - ${models[x][1]}`
    }
    var Prompt = prompt(message)
    var result = models[Number(Prompt) - 1]
    if (result == undefined && Prompt != null) {
        alert('Invaild Input')
        result = models[0]
        setmodel()
    }
    window.model = result[0]
}

function run() {
    var prompt = document.getElementById('prompt').value
    if (prompt == "") { return alert('Prompt cannot be blank') }
    window.Loaded = 1
    document.getElementById('prompt').value = ''
    document.getElementById('prompt').setAttribute('placeholder', prompt)
    callAPI(`/Utilities/AI Chat/prompt`, {'username':data.Cookie.get('username'), 'auth':data.Cookie.get('auth'), 'prompt':prompt, 'model':model, 'chat':1}).then(t => {
        //window.Loaded = 2
        //window.response = t.response
        //window.jsonid = t.id
        document.getElementById('response').innerHTML = JSON.stringify(t)
    })
}
/*
setInterval(() => {
    window.LoadingDotCount = {true:0, false:LoadingDotCount+1} [LoadingDotCount >= 4]
    document.getElementById('response').innerHTML = { 0:'Awaiting Prompt ', 1:'Generating ', 2:response}[Loaded] + ['.', '..', '...', '....', '.....'][LoadingDotCount]
}, 300)*/