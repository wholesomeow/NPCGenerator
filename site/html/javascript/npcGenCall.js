document.getElementById('npcGenCall').addEventListener('click', npcGenCall);

function npcGenCall() {
    fetch('http://127.0.0.1:5000/npcGen')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        console.log(data);
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                const newDiv = document.createElement('div');
                const newContent = document.createTextNode(key + ": " + data[key])
                newDiv.appendChild(newContent);
                const currentDiv = document.getElementById('npcData');
                document.body.insertBefore(newDiv, currentDiv);
            }
        }
    })
    .catch(function(error) {
        console.log(error);
    })
}