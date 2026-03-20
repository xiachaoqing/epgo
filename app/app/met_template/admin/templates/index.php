<?php

defined('IN_MET') or exit('No permission');
$head_tab_active=isset($data['head_tab_active'])?$data['head_tab_active']:0;
$head_tab=array(
	array('title'=>"其他模板",'url'=>'app/met_template/other'),

);
$head_tab_ajax = 1;
?>
<include file="pub/head_tab" />