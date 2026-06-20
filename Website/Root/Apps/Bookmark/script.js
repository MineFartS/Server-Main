
authorize()

data = {

    'read': (e) => {

        API.auth('/Apps/Bookmark/read', {x:e.id})
            .then(t => e.value = t)

    },

    'save': (e) => {

        API.auth(
            '/Apps/Bookmark/save',
            {
                'x': e.id,
                'value': e.value
            }
        )

    }

}

// Load data for all elements
document.querySelectorAll('input[type="text"]').forEach((e) => data.read(e));
