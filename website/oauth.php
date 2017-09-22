<?php session_start();
include 'oauthfunctions.php';
include 'botfunctions.php';

define('OAUTH2_CLIENT_ID', 'mje53ch80y8kzhppreusp1hax1s6iz');
define('OAUTH2_CLIENT_SECRET', 'xthja1zsiodjb7mk24ooibmfkr63ol');
define('REDIRECT_URI', 'http://localhost/oauth.php');

$localServerBotDashboard = 'dashboard.php';
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

if(session('access_token')) {
  if(!session('username')) {
    $userInfo = apiRequest($userURL);
    $_SESSION['username'] = $userInfo->data[0]->login;
  }

  sendTwitchBot();
  header('Location: ' . $localServerBotDashboard);
  die();
} else {
  echo '<h3>Not logged in</h3>';
  echo '<p><a href="?action=login">Log In</a></p>';
}
?>