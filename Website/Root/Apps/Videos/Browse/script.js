
const playerurl = '/Apps/Videos/Player?id='

API.call('/Apps/Videos/List').then(items => 
    postSearch(term => {
        
        let results = []

        for (let i of items) {

            if (i.Title[0].toLowerCase().includes(term)) {
                results.push( new TextResult(
                    title = i.Title, 
                    callback = (playerurl + i.id)
                ) )
            }

        }

        return results
        
    })
)

