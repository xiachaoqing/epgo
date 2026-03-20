<?php
# MetInfo Enterprise Content Management System


defined('IN_MET') or exit('No permission');

/**
 * 系统标签类
 */

class label
{
    /**
     * 为字段赋值
     * @param  string $module模型名称
     * @param  array $input 所有输入变量
     * @return array          合法的页面变量
     */
    public function get($module)
    {
        global $_M;
        return load::mod_class($module . '/include/class/' . $module . '_label.class.php', 'new');
    }
}

# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>
