
fetch('search.json').then(r => r.json()).then(items => 
    postSearch(term => {
        
        let results = []

        for (let i of items) {

            if (i.Visible && i.Title.toLowerCase().includes(term)) {
                results.push( new TextResult(i.Title, i.URL) )
            }

        }

        return results
        
    })
)

