<?php session_start();
include 'oauthfunctions.php';

if(!$_SESSION['username'] || !checkAuth()) {
	echo "not logged in";
} else {
	echo "logged in as " . $_SESSION['username'];
}
?>