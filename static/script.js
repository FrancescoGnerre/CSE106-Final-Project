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
