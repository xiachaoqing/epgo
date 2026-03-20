<?php
# MetInfo Enterprise Content Management System 
 

defined('IN_MET') or exit('No permission');

load::sys_class('admin');
load::sys_func('file');
load::sys_func('array');

class patch extends admin
{
    public function docheckEnv()
    {
        global $_M;
        $handle = load::sys_class('handle', 'new');
        $data = array(
            'data' => $handle->checkFunction(),
            'dirs' => $handle->checkDirs()
        );
        return $data;
    }
}

# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>