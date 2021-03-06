var curr_name = "";
var curr_password = "";
var home_password = "";
var list = document.getElementById('files');
var lastid = 0;

// sets name to be inputted username
function setName(){
	curr_name = document.getElementById("user_name").value;
	consolePrint(curr_name)
}
// sets password to be inputted password
function setPassword(){
	curr_password = document.getElementById("password").value;
	consolePrint(curr_password)
}
// sets home password to be the real password
function setPassword(newPassword){
    home_password = newPassword;
}
// prints for debugging
function consolePrint(x){
	console.log(x);
}

// When user logs out
function logOut() {
	$.ajax({
        url: "https://alexholt54.pythonanywhere.com/logout",
        type: "GET",
        success: function(response){
            window.location.href = "https://alexholt54.pythonanywhere.com/"
        },
        error: function(status, error){
            alert(error)
        }
    });
}

// When user goes to registration page
function toRegistration() {
	window.location.href = "https://alexholt54.pythonanywhere.com/registration";
}

function toFilePage() {
	window.location.href = "https://alexholt54.pythonanywhere.com/files";
}

function toHomePage() {
	window.location.href = "https://alexholt54.pythonanywhere.com/home";
}

function toUserPage() {
    user = document.getElementById("username").value;
    window.location.href = "https://alexholt54.pythonanywhere.com/user/" + user;
}

// When user creates a new user
function registerUser() {
	let username = $("#newUsername").val();
    let password = $("#newPassword").val();
	let name = $("#newName").val()
    if (username !== "" && password !== "" && name !== "") {
        $.ajax({
            url: window.location.href,
            type: "POST",
            data: JSON.stringify({"username" : username, "password" : password, "name" : name}),
            contentType: "application/JSON",
            success: function(response){
                alert("New Account Created! You can now log in!")
                window.location.href = "https://alexholt54.pythonanywhere.com/"
            },
            error: function(status, error){
                alert(error)
            }
        });
    }
}

// When user logs in
function logIn() {
	let username = $("#username").val();
    let password = $("#password").val();
	if (username !== "" && password !== "") {
		$.ajax({
            url: window.location.href,
            type: "POST",
            data: JSON.stringify({"username" : username, "password" : password}),
            contentType: "application/JSON",
            success: function(response){
                window.location.href = "https://alexholt54.pythonanywhere.com/" + response
            },
            error: function(status, error){
                alert(error)
            }
        });
	}
}

function makePieGraph() {
    let title = $("#graphTitle").val();
    let row = $("#rowNumber").val();
    alert(title + row)
    if (title !== "" && row !== "") {
        $.ajax({
            url: window.location.href,
            type: "POST",
            data: JSON.stringify({"title" : title, "row" : parseInt(row), "type" : "pie"}),
            contentType: "application/JSON",
            success: function(response){
                alert("Graph Made!")
            },
            error: function(status, error){
                alert(error)
            }
        });
    }
}

function makeBarGraph() {
    let title = $("#bTitle").val();
    let row = $("#bRowNumber").val();
    let xlabel = $("#xlabelBar").val();
    let ylabel = $("#ylabelBar").val();

    if (title !== "" &&  row !== "" &&  xlabel !== "" && ylabel !== "") {
        $.ajax({
            url: window.location.href,
            type: "POST",
            data: JSON.stringify({"title" : title, "row" : parseInt(row), "xlabel" : xlabel, "ylabel" : ylabel, "type" : "bar"}),
            contentType: "application/JSON",
            success: function(response){
                alert("Graph Made!")
            },
            error: function(status, error){
                alert(error)
            }
        });
    }
}

function makeLineGraph() {
    let title = $("#lTitle").val();
    let legend = $("#llegname").val();
    let numcols = $("#numcols").val();
    let xlabel = $("#xlabelLine").val();
    let ylabel = $("#ylabelLine").val();

    if (title !== "" &&  legend !== "" &&  xlabel !== "" && ylabel !== "" && numcols !== "") {
        $.ajax({
            url: window.location.href,
            type: "POST",
            data: JSON.stringify({"title" : title, "legend" : legend, "numcols" : parseInt(numcols), "xlabel" : xlabel, "ylabel" : ylabel, "type" : "line"}),
            contentType: "application/JSON",
            success: function(response){
                alert("Graph Made!")
            },
            error: function(status, error){
                alert(error)
            }
        });
    }
}

function toAccount(){
	window.location.href = "https://alexholt54.pythonanywhere.com/user"
}

function backToFiles() {
    window.location.href = "https://alexholt54.pythonanywhere.com/files";
}

function uploadFile() {
	// Make call to server to upload file
	let form_data = new FormData($("#upload-file")[0]);
	$.ajax({
		url: window.location.href,
		type: "POST",
		data: form_data,
		contentType: false,
		processData: false,
        cache: false,
		success: function(response){
            alert("File Uploaded!")
            window.location.href = "https://alexholt54.pythonanywhere.com/files"
		},
		error: function(status, error){
            alert(error)
            window.location.href = "https://alexholt54.pythonanywhere.com/files"
		}
	});
}

function updateFiles(i) {
    var filename = document.getElementById(i).value;
    var entry = document.createElement('li');
    entry.appendChild(document.createTextNode(filename));
    entry.setAttribute('id','item'+lastid);
    var removeButton = document.createElement('button');
    removeButton.appendChild(document.createTextNode("remove"));
    removeButton.setAttribute('onClick','removeFile("'+'item'+lastid+'","'+filename+'")');
    entry.appendChild(removeButton);
    lastid+=1;
    list.appendChild(entry);
}