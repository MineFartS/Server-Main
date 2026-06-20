
// =====================================================================
// ELEMENTS:

    e['human'] = document.getElementById('Human')
    e['dog'] = document.getElementById('Dog')

    document.title = `'${parameters.name}' Age Calculator`
    e.title.textContent = document.title

// =====================================================================
// -:

    let [y, m, d] = parameters.dob.split('-')

    const DOB = new Date(
        year = y,
        month = m-1,
        day = d
    )

    const now = new Date()

    function setValues(el, age, bday) {
        el.textContent = 
`${el.id} Age:
${age.getFullYear()-1970}y ${age.getMonth()}m ${age.getDay()}d

Next BDay: 
${bday.toDateString().split(' ').slice(1, 4).join(' ')}`

    }

    const YearMS = 31556952000

// =====================================================================
// HUMAN YEARS:

    let nbday = new Date(DOB)

    while (nbday.getTime() < now.getTime()) {
        nbday.setFullYear(nbday.getFullYear() + 1)
    }

    setValues(
        
        el = e.human,

        age = new Date(now.getTime() - DOB.getTime()),

        bday = nbday

    )

// =====================================================================
// DOG YEARS:

    // https://www.nbcnews.com/health/health-news/how-old-your-dog-new-equation-shows-how-calculate-its-n1233459#:~:text=the%20equation,.

    let
    hYears = (now.getTime() - DOB.getTime()) / YearMS;
    dYears = (16 * Math.log(hYears)) + 31

    // # of Dog years between now and next dog bday
    now_nbday = Math.log(hYears) - Math.log(hYears-1)

    // # of Human years between now and next dog bday
    now_nbday = Math.exp((now_nbday-31)/16)

    // # of Milliseconds between now and next dog bday
    now_nbday = now_nbday * YearMS

    // Next Dog bday
    nbday = new Date(now.getTime() + now_nbday)

    setValues(

        el = e.dog,

        age = new Date(dYears * YearMS),

        bday = nbday

    )

// =====================================================================
