function getTaskDataAdd(){
    var mymap = {}  
    
    // Error checking later
    var taskid = parseInt(document.getElementById("task_number").value);
    if (isNaN(taskid)){
      document.getElementById('query_response').innerHTML = "Not a valid id"
      mymap['id'] = -1
      return mymap; 
    }
    mymap['id'] = document.getElementById("task_number").value
    let tmp = document.getElementById("task_data").value
    let tmp2 = tmp.split(',');

    if (tmp2.length != 2){
      document.getElementById('query_response').innerHTML = "Invalid input"
      mymap['id'] = -1
      return mymap;
    }

    mymap['desc'] = tmp2[0];
    var userid = parseInt(tmp2[1]);

    if (isNaN(userid)){
      document.getElementById('query_response').innerHTML = "Not a valid user id"
      mymap['id'] = -1
      return mymap; 
    }
    mymap['user_id'] = tmp2[1];

    return mymap
}

function getTaskID(){
    var mymap = {}  

    var taskid = parseInt(document.getElementById("task_number").value);
    if (isNaN(taskid)){
      document.getElementById('query_response').innerHTML = "Not a valid id"
      mymap['id'] = -1
      return mymap; 
    }

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

 function listNonCompleteTasks(data){
   var tmp = '<h3> Non-completed tasks </h3> <br> '

   if (data.length == 1 && data[0] == "none"){
     document.getElementById('query_response').innerHTML = "No non-completed tasks in database"
     return
 }

  console.log("List non-completed tasks, found " + data.length.toString() + " task(s)")

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
  fetch('/task', {
    method: 'GET', 
    headers: {
      'Content-Type': 'application/json'
    } 
  })
  .then(data => data.json())
  .then(data => listNonCompleteTasks(data))
  .catch(err => console.log('Non-complete Task  ' + err))

}

function CompleteTask(){

  var bdy = getTaskID();

  if (parseInt(bdy['id']) < 0)
    return;

    fetch('/task', {
        method: 'PUT', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(bdy) 
      })
      .then(data => data.json())
      .then(data => document.getElementById('query_response').innerHTML = data.message)
      .catch(err => console.log('Complete task ' + err))
}

function addTask(){
    
    var bdy = getTaskDataAdd();

    if (parseInt(bdy['id']) < 0)
      return;

    fetch('/task', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(bdy) 
      })
      .then(data => data.json())
      .then(data => document.getElementById('query_response').innerHTML = data.message)
      .catch(err => console.log('Task add: ' + err))
}

function deleteTask(){

  var bdy = getTaskID();

  if (parseInt(bdy['id']) < 0)
    return;

  fetch('/task', {
      method: 'DELETE', 
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(bdy)  
      })
      .then(data => data.json())
      .then(data => document.getElementById('query_response').innerHTML = data.message)
      .catch(err => console.log('Task delete ' + err))
}


