function getTaskDataAdd(){
    var mymap = {}  
    
    // Error checking later
    mymap['id'] = document.getElementById("task_number").value;
    let tmp = document.getElementById("task_data").value
    let tmp2 = tmp.split(',');
    mymap['desc'] = tmp2[0];
    mymap['complete'] = tmp2[1];
    mymap['user_id'] = tmp2[2];

    return mymap
}

function getTaskID(){
    var mymap = {}  
    mymap['id'] = document.getElementById("task_number").value;
    return mymap;
}

function listTask(data){
    var tmp = '<h3> Task data </h3> <br> '

    if (data.length == 1 && data[0] == "none"){
        document.getElementById('query_response').innerHTML = "No tasks in database"
        return
    }

    if (data.length == 1 && parseInt(data[0]) <= 0){
        tmp = "No task with id " + -parseInt(data[0]) +" found";
        document.getElementById('query_response').innerHTML = tmp;
        console.log("Listtask: No task with id " + -parseInt(data[0]) +" found")
        return
    }

    console.log("Listtask, found " + data.length.toString() + " task(s)")

    for(let i=0; i < data.length; i++){
        let tmp2 = data[i].toString().split(',');
        for(let j=0; j<tmp2.length;j++) 
            tmp += tmp2[j] + '<pre></pre>'; 
        tmp += '<br>'; 
    }
    document.getElementById('query_response').innerHTML = tmp;
 }

    
function listTasks(){
    
    var url = '/listtask/' + document.getElementById("task_number").value
    fetch(url, {
          method: 'GET', 
          headers: {
            'Content-Type': 'application/json'
          } 
        })
        .then(data => data.json())
        .then(data => listTask(data))
        .catch(err => console.log('Task get ' + err))
} 

function listNonCompletedTasks(){
    console.log("Listing non-completed tasks")
    document.getElementById('query_response').innerHTML = "Here comes a list of uncompleted tasks";
}

function CompleteTask(){
    fetch('/task', {
        method: 'PUT', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(getTaskID()) 
      })
      .then(data => data.json())
      .then(data => document.getElementById('query_response').innerHTML = data.message)
      .catch(err => console.log('Complete task ' + err))
}

function addTask(){
    
    fetch('/task', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(getTaskDataAdd()) 
      })
      .then(data => data.json())
      .then(data => document.getElementById('query_response').innerHTML = data.message)
      .catch(err => console.log('Task add: ' + err))
}

function deleteTask(){
        fetch('/task', {
            method: 'DELETE', 
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(getTaskID())  
          })
          .then(data => data.json())
          .then(data => document.getElementById('query_response').innerHTML = data.message)
          .catch(err => console.log('Task delete ' + err))
}


