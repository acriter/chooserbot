<?php session_start();
$serverUrl = 'localhost:5000';
$params = array(
	'foo' => 'bar'
);

$authpage = $serverUrl . '?' . http_build_query($params);
//header('Location: ' . $authpage);
die();
?>