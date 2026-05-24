function createForms() {

    let count = document.getElementById("studentCount").value;

    let formsContainer = document.getElementById("formsContainer");

    formsContainer.innerHTML = "";

    for(let i = 1; i <= count; i++) {

        formsContainer.innerHTML += `

        <div class="studentForm">

            <h2>Student ${i}</h2>

            <div class="inputGrid">

                <input type="text"
                       id="name${i}"
                       placeholder="Enter Name">

                <input type="number"
                       id="roll${i}"
                       placeholder="Enter Roll Number">

                <input type="text"
                       id="sub1${i}"
                       placeholder="Subject 1">

                <input type="number"
                       id="m1${i}"
                       placeholder="Marks">

                <input type="text"
                       id="sub2${i}"
                       placeholder="Subject 2">

                <input type="number"
                       id="m2${i}"
                       placeholder="Marks">

                <input type="text"
                       id="sub3${i}"
                       placeholder="Subject 3">

                <input type="number"
                       id="m3${i}"
                       placeholder="Marks">

                <input type="text"
                       id="sub4${i}"
                       placeholder="Subject 4">

                <input type="number"
                       id="m4${i}"
                       placeholder="Marks">

                <input type="text"
                       id="sub5${i}"
                       placeholder="Subject 5">

                <input type="number"
                       id="m5${i}"
                       placeholder="Marks">

            </div>

            <button class="submitBtn"
                    onclick="generateResult(${i})">

                Generate Result

            </button>

        </div>

        `;
    }
}

function generateResult(i) {

    let name = document.getElementById(`name${i}`).value;

    let roll = document.getElementById(`roll${i}`).value;

    let subjects = [
        document.getElementById(`sub1${i}`).value,
        document.getElementById(`sub2${i}`).value,
        document.getElementById(`sub3${i}`).value,
        document.getElementById(`sub4${i}`).value,
        document.getElementById(`sub5${i}`).value
    ];

    let marks = [
        Number(document.getElementById(`m1${i}`).value),
        Number(document.getElementById(`m2${i}`).value),
        Number(document.getElementById(`m3${i}`).value),
        Number(document.getElementById(`m4${i}`).value),
        Number(document.getElementById(`m5${i}`).value)
    ];

    let total = 0;

    for(let j = 0; j < 5; j++) {

        total += marks[j];
    }

    let percentage = total / 5;

    let grade;

    if(percentage >= 90)
        grade = "A";

    else if(percentage >= 75)
        grade = "B";

    else if(percentage >= 60)
        grade = "C";

    else if(percentage >= 50)
        grade = "D";

    else
        grade = "F";

    let resultContainer =
        document.getElementById("resultContainer");

    resultContainer.innerHTML += `

    <div class="studentCard">

        <h2>${name}</h2>

        <p><b>Roll Number:</b> ${roll}</p>

        <table>

            <tr>
                <th>Subject</th>
                <th>Marks</th>
            </tr>

            <tr>
                <td>${subjects[0]}</td>
                <td>${marks[0]}</td>
            </tr>

            <tr>
                <td>${subjects[1]}</td>
                <td>${marks[1]}</td>
            </tr>

            <tr>
                <td>${subjects[2]}</td>
                <td>${marks[2]}</td>
            </tr>

            <tr>
                <td>${subjects[3]}</td>
                <td>${marks[3]}</td>
            </tr>

            <tr>
                <td>${subjects[4]}</td>
                <td>${marks[4]}</td>
            </tr>

        </table>

        <h3>Total Marks: ${total}/500</h3>

        <h3>Percentage: ${percentage}%</h3>

        <h3>Grade: ${grade}</h3>

    </div>

    `;
}