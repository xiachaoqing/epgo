<?php
// Legacy empty feature page: consolidate its historical URL into the maintained About page.
if (!headers_sent()) {
    header('Location: /about/', true, 301);
    exit;
}
# MetInfo Enterprise Content Management System 
# Copyright (C) MetInfo Co.,Ltd (http://www.mituo.cn). All rights reserved. 
require_once '../about/index.php';
# This program is an open source system, commercial use, please consciously to purchase commercial license.
# Copyright (C) MetInfo Co., Ltd. (http://www.mituo.cn). All rights reserved.
?>
