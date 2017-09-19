<?php session_start();
$serverUrl = 'http://localhost:5000/login';
$params = array(
	'foo' => 'bar'
);

$authpage = $serverUrl . '?' . http_build_query($params);
header('Location: ' . $authpage);
die();
?>