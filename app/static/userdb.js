function updateTarget(){
    console.log(document.getElementById("target").value);
}

function listUser(data){
    var tmp = '<h3> User data </h3> <br> '

    if (data.length == 1 && data[0] == "none"){
        document.getElementById('query_response').innerHTML = "No users in database"
        return
    }

    if (data.length == 1 && parseInt(data[0]) <= 0){
        tmp = "No user with id " + -parseInt(data[0]) +" found";
        document.getElementById('query_response').innerHTML = tmp;
        console.log("Listuser: No user with id " + -parseInt(data[0]) +" found")
        return
    }

    console.log("Listusers, found " + data.length.toString() + " user(s)")

    for(let i=0; i < data.length; i++){
        let tmp2 = data[i].toString().split(',');
        for(let j=0; j<tmp2.length;j++) 
            tmp += tmp2[j] + '<pre></pre>'; 
        tmp += '<br>'; 
    }
    document.getElementById('query_response').innerHTML = tmp;
 }

 // Reads values from input fields in user database section
function getUserData(){
    var mymap = {}  
    var tmp = document.getElementById("user_id").value
    if (tmp === "all")
        mymap['id'] = tmp;
    else {
        mymap['id'] = tmp;
        let tmp2 = document.getElementById("user_data").value
        let tmp3 = tmp.split(',');
        mymap['name'] = tmp3[0];
        mymap['password'] = tmp3[1];
        mymap['admin_stat'] = tmp3[2];
    }
    return mymap
}

function getUserID(){
    var mymap = {}  
    mymap['id'] = document.getElementById("user_id").value;
    return mymap;
}


// Get user(s)
function getUser(){
    var url = '/listuser/' + document.getElementById("user_id").value
    fetch(url, {
          method: 'GET', 
          headers: {
            'Content-Type': 'application/json'
          } 
        })
        .then(data => data.json())
        .then(data => listUser(data))
        .catch(err => console.log('Restful get ' + err))
}