<?php
# MetInfo Enterprise Content Management System


defined('IN_MET') or exit('No permission');

load::mod_class('base/base_label');

/**
 * news标签类
 */

class news_label extends base_label
{
    public $lang; //语言

    /**
     * 初始化
     */
    public function __construct()
    {
        global $_M;
        $this->construct('news', $_M['config']['met_news_list']);
    }

}

# This program is an open source system, commercial use, please consciously to purchase commercial license.

