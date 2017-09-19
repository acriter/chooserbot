<?php session_start();
define('OAUTH2_CLIENT_ID', 'mje53ch80y8kzhppreusp1hax1s6iz');
define('OAUTH2_CLIENT_SECRET', 'xthja1zsiodjb7mk24ooibmfkr63ol');
define('REDIRECT_URI', 'http://localhost/oauth.php');

$pythonServerURL = 'http://localhost:5000/join';
$authorizeURL = 'https://api.twitch.tv/kraken/oauth2/authorize';
$tokenURL = 'https://api.twitch.tv/kraken/oauth2/token';
$userURL = 'https://api.twitch.tv/helix/users';

// Start the login process by sending the user to Twitch's authorization page
if(get('action') == 'login') {
  // Generate a random hash and store in the session for security
  $_SESSION['state'] = hash('sha256', microtime(TRUE).rand().$_SERVER['REMOTE_ADDR']);
  unset($_SESSION['access_token']);

  $params = array(
    'client_id' => OAUTH2_CLIENT_ID,
    'redirect_uri' => REDIRECT_URI,
    'response_type' => 'code',
    'scope' => 'user:edit user:read:email chat_login',
    'state' => $_SESSION['state']
  );

  // Redirect the user to Twitch's authorization page
  $authpage = $authorizeURL . '?' . http_build_query($params);
  header('Location: ' . $authpage);
  die();
}

// When Twitch redirects the user back here, there will be a "code" and "state" parameter in the query string
if(get('code')) {
  // Verify the state matches our stored state
  if(!get('state') || $_SESSION['state'] != get('state')) {
    header('Location: ' . $_SERVER['PHP_SELF']);
    die();
  }

  // Exchange the auth code for a token
  $token = apiRequest($tokenURL, array(
    'client_id' => OAUTH2_CLIENT_ID,
    'client_secret' => OAUTH2_CLIENT_SECRET,
    'redirect_uri' => REDIRECT_URI,
    'grant_type' => 'authorization_code',
    'state' => $_SESSION['state'],
    'code' => get('code')
  ));
  $_SESSION['access_token'] = $token->access_token;

  header('Location: ' . $_SERVER['PHP_SELF']);
  die();
}

echo '<pre>';
var_dump($_SESSION);
echo '</pre>';
if(session('access_token')) {
  if(!session('username')) {
    $userInfo = apiRequest($userURL);
    $_SESSION['username'] = $userInfo->data[0]->login;
  }
  echo '<h3>Logged In as ' . $_SESSION['username'] . '!</h3>';
  sendTwitchBot();
} else {
  echo '<h3>Not logged in</h3>';
  echo '<p><a href="?action=login">Log In</a></p>';
}

function sendTwitchBot() {
  $ch = curl_init($pythonServerURL);
  $headers[] = 'Accept: application/json';
  curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(
    array(
    'username' => $_SESSION['username']
    )));
  curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

  $response = curl_exec($ch);

  echo "somewhere at least\n";
  echo "\nresponse: " . $response;
  #return json_decode($response);
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

function session($key, $default=NULL) {
  return array_key_exists($key, $_SESSION) ? $_SESSION[$key] : $default;
}

?>