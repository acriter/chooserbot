<?php session_start();
include_once 'oauthfunctions.php';

$pythonServerBaseURL = 'http://localhost:5000';
$pythonServerBotJoin = $pythonServerBaseURL . '/join';
$pythonServerBotChangeQuestion = $pythonServerBaseURL . '/setquestion';

if(post('question')) {
	//TODO: add auth
	$ch = curl_init($pythonServerBotChangeQuestion);
	$headers[] = 'Accept: application/json';
  	curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(
    array(
    	'question' => post('question')
    )));
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

	$response = curl_exec($ch);
	return json_decode($response);
}

if(post('options')) {
}

function test() {
	echo "did the thing";
}

function sendTwitchBot() {
	$ch = curl_init($pythonServerBotJoin);
	$headers[] = 'Accept: application/json';
	curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(
		array(
			'username' => $_SESSION['username']
		)));
	curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
	$response = curl_exec($ch);
	return json_decode($response);
}
?>