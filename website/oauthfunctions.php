<?php session_start();

function checkAuth() {
  if(!session('access_token')) {
    return false;
  }

  $ch = curl_init('https://api.twitch.tv/kraken');
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);

  $headers[] = 'Accept: application/vnd.twitchtv.v5+json';

  if(session('access_token')) {
    $headers[] = 'Authorization: OAuth ' . session('access_token');
    $headers[] = 'Client-ID: ' . OAUTH2_CLIENT_ID;
  }

  curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

  $response = curl_exec($ch);
  $response = json_decode($response);
  return $response->token->valid;
}

function apiRequest($url, $post=FALSE, $headers=array()) {
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);

  if($post)
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post));

  $headers[] = 'Accept: application/json';

  if(session('access_token')) {
    $headers[] = 'Authorization: Bearer ' . session('access_token');
    $headers[] = 'Client-ID: ' . OAUTH2_CLIENT_ID;
  }

  curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

  $response = curl_exec($ch);
  return json_decode($response);
}

function get($key, $default=NULL) {
  return array_key_exists($key, $_GET) ? $_GET[$key] : $default;
}

function post($key, $default=NULL) {
  return array_key_exists($key, $_POST) ? $_POST[$key] : $default;
}

function session($key, $default=NULL) {
  return array_key_exists($key, $_SESSION) ? $_SESSION[$key] : $default;
}

?>