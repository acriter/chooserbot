<?php session_start(); 
include_once 'oauthfunctions.php';
?>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $("#setQuestionButton").click(function(){
    	$("#div1").fadeIn();
    	var questionText = $("#questionTextField").val();
        var ajaxurl = 'http://localhost/botfunctions.php/';
        data =  {'question': questionText};
        $.post(ajaxurl, data, function (response) {
        	alert(response);
        });
    });
});
</script>
</head>
<body>

<?php
if(!$_SESSION['username'] || !checkAuth()) {
	echo "not logged in";
	?>
	<form action="http://oauth.php/?action=login" method="get">
  		<input type="text" value="Login"/>
  		<input type="submit" />
	</form>
<?php
	
} else {
	echo "logged in as " . $_SESSION['username'];
}
?>

<br />
Set question text: <input id="questionTextField" type="text" placeholder="Which deck should I play?">
<button id="setQuestionButton">Submit</button>

<div id="div1" style="width:80px;height:80px;display:none;background-color:red;"></div><br>

</body>
</html>