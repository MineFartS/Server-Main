
const pages = []

let page = null

e['last'] = document.getElementById('last')
e['next'] = document.getElementById('next')
e['text'] = document.getElementById('text')
e['image'] = document.getElementById('image')
e['pageNum'] = document.getElementById('pageNum')

fetch('index.json').then(r => r.json()).then(items => {

    for (x in items) {
        
        let i = items[x]

        if (!isNaN(Number(i.Title))) {

            pages.push(i.URL)

        }
    
    }

    setPage(1)

})

function setPage(x) {

    page = x

    // If on first page
    if (page == 1) {
        // Hide last page button
        e.last.setAttribute('style', 'display: none')
    } else {
        // Show last page button
        e.last.setAttribute('style', '')
    }

    // If on last page
    if (page == pages.length) {
        // Hide next page button
        e.next.setAttribute('style', 'display: none')
    } else {
        // Show next page button
        e.next.setAttribute('style', '')
    }
    
    // Get url of folder with page content
    let url = pages[page-1]

    // Fetch page text
    fetch(url + 'text.txt').then(r => r.text()).then(t => {

        // Set Text element to page text
        e.text.textContent = t

    })

    //
    e.image.setAttribute('src', url+'image.png?raw=true')

    e.pageNum.textContent = `${page}/${pages.length}`

}