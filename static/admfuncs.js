function getAllUsers(){
    var url = '/listuser/all'
    fetch(url, {
          method: 'GET', 
          headers: {
            'Content-Type': 'application/json'
          } 
        })
        .then(data => data.json())
        .then(data => listUser(data))
        .catch(err => console.log('List all users: ' + err))
    }

// Delete user(s)
function deleteUser(){ 
    fetch('/editusers', {
        method: 'DELETE', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({'id': document.getElementById("admpage_userid").value})  
      })
      .then(data => data.json())
      .then(data => document.getElementById('adm_query_response').innerHTML = data.message)
      .catch(err => console.log('Delete user' + err))
}

// Modify admin status of specified user
function toggleAdmStatus(){
    fetch('/editusers', {
        method: 'PUT', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({'id': document.getElementById("admpage_userid").value}) 
      })
      .then(data => data.json())
      .then(data => document.getElementById('adm_query_response').innerHTML = data.message)
      .catch(err => console.log('Modify admin status ' + err))
}