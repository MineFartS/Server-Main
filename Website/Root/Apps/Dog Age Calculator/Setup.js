
e['content'] = document.getElementById('content')

e.content.innerHTML = `
    <div class="form">
        <form action="." method="get">

            <label for="name">Name:</label>
            <br>
            <input type="text" name="name" placeholder="Enter your name">

            <br>

            <label for="dob">Birthday:</label>
            <br>
            <input type="date" name="dob" placeholder="">

            <br>

            <input type="submit" value="Calculate">

        </form>
    </div>
`