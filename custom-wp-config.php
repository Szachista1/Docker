<?php


// Lista serwerów po NAZWACH z docker-compose 
$db_servers = ['mysql_master:3306', 'mysql_slave:3306'];

$connected = false;
foreach ($db_servers as $server) {
    // Sprawdzamy czy serwer odpowiada
    $fp = @fsockopen(parse_url("tcp://$server", PHP_URL_HOST), 3306, $errno, $errstr, 1);
    if ($fp) {
        define('DB_HOST', $server);
        fclose($fp);
        $connected = true;
        break;
    }
}

if (!$connected) {
    die('<h1>Error: Service Temporarily Unavailable (DB Connection Failed)</h1>');
}

// Pobieranie danych ze zmiennych środowiskowych (.env)
define( 'DB_NAME', getenv('WORDPRESS_DB_NAME') );
define( 'DB_USER', getenv('WORDPRESS_DB_USER') );
define( 'DB_PASSWORD', getenv('WORDPRESS_DB_PASSWORD') );

// Reszta to standardowy config WP...
define( 'DB_CHARSET', 'utf8' );
define( 'DB_COLLATE', '' );
$table_prefix = 'wp_';
define( 'WP_DEBUG', false );
if ( ! defined( 'ABSPATH' ) ) {
    define( 'ABSPATH', __DIR__ . '/' );
}
require_once ABSPATH . 'wp-settings.php';