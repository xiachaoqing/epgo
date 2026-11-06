<?php
# MetInfo Enterprise Content Management System

// The hits endpoint only records view counters and has no indexable content.
// Keep crawler requests from treating its tiny response as a public page.
header('X-Robots-Tag: noindex, nofollow');

$a = @$_GET['a'] ? $_GET['a'] : 'dohits';

define('M_NAME', 'hits');
define('M_MODULE', 'web');
define('M_CLASS', 'hits');
define('M_ACTION', $a);
require_once '../app/system/entrance.php';

# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>
