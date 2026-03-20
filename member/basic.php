<?php
# MetInfo Enterprise Content Management System 
 

//接口
if(@!$_GET['a'])$_GET['a']="doindex";
@define('M_NAME', 'user');
@define('M_MODULE', 'web');
@define('M_CLASS', 'profile');
@define('M_ACTION', $_GET['a']);
require_once '../app/system/entrance.php';
# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>