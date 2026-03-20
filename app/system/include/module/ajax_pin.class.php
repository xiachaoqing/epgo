<?php
# MetInfo Enterprise Content Management System 
 

defined('IN_MET') or exit('No permission');

class ajax_pin
{
    public function dogetpin()
    {
        global $_M;
        $random = $_GET['random'];
        load::sys_class('pin', 'new')->create_pin($random);
    }
}

# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>