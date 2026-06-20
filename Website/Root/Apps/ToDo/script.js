
e['boxes'] = document.getElementById('boxes')

data = {

    'read': (e) => {

        API.auth('/Apps/Bookmark/read', {x:e.id+3})
            .then(t => e.value = t)

    },

    'save': (e) => {

        API.auth(
            '/Apps/Bookmark/save',
            {
                'x': e.id+3,
                'value': e.value
            }
        )

    },

    'clear': (e) => {

        e.value = ''

        data.save(e)

        e.destroy()

    }


}
