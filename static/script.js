var curr_name = "";
var curr_password = "";
var home_password = "";

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
        url: "http://127.0.0.1:5000/logout",
        type: "GET",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/"
        }, 
        error: function(status, error){
            alert(error)
        }
    });
}

// When user goes to registration page
function toRegistration() {
	window.location.href = "http://127.0.0.1:5000/registration";
}

function toFilePage() {
	window.location.href = "http://127.0.0.1:5000/files";
}

function toHomePage() {
	window.location.href = "http://127.0.0.1:5000/home";
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
                window.location.href = "http://127.0.0.1:5000/"
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
                window.location.href = "http://127.0.0.1:5000/" + response
            }, 
            error: function(status, error){
                alert(error)
            }
        });
	}
}

function makePieGraph() {

}

function makeBarGraph() {
    
}

function makeLineGraph() {
    
}

function backToFiles() {
    window.location.href = "http://127.0.0.1:5000/files";
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
            window.location.href = "http://127.0.0.1:5000/files"
		}, 
		error: function(status, error){
            alert(error)
            window.location.href = "http://127.0.0.1:5000/files"
		}
	});
}

$('.delete').on('click', function(){
    $(this).parent().remove();
    console.log($(this).parent().find(".fuckingthing").html())
  });