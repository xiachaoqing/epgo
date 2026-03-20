<?php
# MetInfo Enterprise Content Management System


defined('IN_MET') or exit('No permission');

load::mod_class('base/base_label');

class img_label extends base_label
{
    public function __construct()
    {
        global $_M;
        $this->construct('img', $_M['config']['met_img_list']);
    }

}

# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>
