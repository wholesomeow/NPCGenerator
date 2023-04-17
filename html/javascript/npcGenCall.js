'use strict';

document.getElementById('npcGenCall').addEventListener('click', npcGenCall);


function npcGenCall() {
    console.log('API Call Initiated')
    fetch('http://127.0.0.1:5000/npcGen')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        console.log('Processing Started')
        for (let key in data) {
            document.getElementById(key).innerHTML = data[key];
        }
        console.log('Processing Finished')
    })
    .catch(function(error) {
        console.log(error);
    })
}