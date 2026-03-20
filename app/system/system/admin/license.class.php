<?php
# MetInfo Enterprise Content Management System


defined('IN_MET') or exit('No permission');

load::sys_class('admin');

class license extends admin
{

    public function __construct()
    {
        parent::__construct();
    }

    public function doLicenseList()
    {
        global $_M;
        if (!$_M['config']['met_agents_metmsg']) {//显示官方信息
            return;
        }

        $list = self::licenseList();
        return $list;
    }

    /**
     * 获取系统插件开源许可协议
     * @param string $dir
     * @param int $level
     * @return array
     */
    protected function licenseList()
    {
        $dir_list = array(
            PATH_PUBLIC . 'plugins/',
            PATH_PUBLIC . 'web/plugins/',
            PATH_PUBLIC . 'admin_old/plugins/',
            PATH_PUBLIC . 'fonts/',
            PATH_SYS_CLASS,
            PATH_SYS_MODULE
        );
        $list = '';
        foreach ($dir_list as $key => $value) {
            if ($list) {
                $list = array_merge($list, $this->getPluginsLicenseByDir($value));
            } else {
                $list = $this->getPluginsLicenseByDir($value);
            }
        }
        return $list;
    }

    public function doGetLicense()
    {
        global $_M;
        $id = $_M['form']['id'];

        $list = self::licenseList();
        if (isset($list[$id])) {
            $path = PATH_WEB . $list[$id]['license_url'];
            $data = file_get_contents($path);
        }

        $this->success($data);
    }

    /**
     * @param string $dir
     * @return array
     */
    protected function getPluginsLicenseByDir($dir = '')
    {
        global $_M;
        $list = array();
        $suffix = strstr($dir, 'app/system/include/class/') || strstr($dir, 'app/system/include/module/') ? 'php' : 'js';
        $handle = scan_dir($dir);
        sort($handle, SORT_FLAG_CASE | SORT_NATURAL);
        foreach ($handle as $row) {
            $path = PATH_WEB . $row;
            if (is_dir($path)) {
                if (file_exists($path . '/LICENSE')) {
                    $license = array();
                    $license['name'] = $row . '/';
                    $license['license_url'] = $row . '/LICENSE';
                    $list[] = $license;
                } else {
                    $handle_2 = scan_dir($path);
                    sort($handle_2, SORT_FLAG_CASE | SORT_NATURAL);
                    foreach ($handle_2 as $row2) {
                        if (strstr($row2, 'LICENSE')) {
                            $license = array();
                            $license['name'] = str_replace(array('.LICENSE', '-LICENSE', '.MIT', '.LGPLv2.1'), '', $row2) . '.' . $suffix;
                            $license['license_url'] = $row2;
                            $list[] = $license;
                        }
                    }
                }
            } else {
                if (strstr($row, 'LICENSE')) {
                    $license = array();
                    $license['name'] = str_replace(array('.LICENSE', '-LICENSE', '.MIT', '.LGPLv2.1'), '', $row) . '.' . $suffix;
                    $license['license_url'] = $row;
                    $list[] = $license;
                }
            }
        }

        return $list;
    }
}

# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>