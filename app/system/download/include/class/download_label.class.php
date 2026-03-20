<?php
# MetInfo Enterprise Content Management System


defined('IN_MET') or exit('No permission');

load::mod_class('base/base_label');

/**
 * download标签类
 */

class download_label extends base_label
{

    /**
     * 初始化
     */
    public function __construct()
    {
        global $_M;
        $this->construct('download', $_M['config']['met_download_list']);
    }
}

# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>
