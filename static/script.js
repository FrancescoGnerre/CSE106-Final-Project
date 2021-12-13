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

// When login button is clicked...
$("#loginbutton").on("click", function(){
    let username = $("#user_name").val();
    let password = $("#password").val()
    if (username !== "" && password !== "") {
        $.ajax({
            url: "http://127.0.0.1:5000/",
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
    else{
        alert('haha')
    }
});