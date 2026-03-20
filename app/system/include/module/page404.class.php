<?php
# MetInfo Enterprise Content Management System 
 

defined('IN_MET') or exit('No permission');

load::sys_class('web');

class page404 extends web
{

    public function dohtml()
    {
        global $_M;
        $this->add_input('module', '404');
        $this->seo_title($_M['config']['met_webname'] . '-404');
        require_once $this->template('tem/404');
    }
}

# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>