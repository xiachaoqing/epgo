<?php
# MetInfo Enterprise Content Management System


defined('IN_MET') or exit('No permission');

load::sys_class('admin');

/**
 * Class transdoc
 */
class transdoc extends admin{

    public function __construct() {
        global $_M;
        parent::__construct();
        $this->docparse = load::sys_class('docparse','new');
        $this->allow_ext = array('docx');
    }

    /**
     *
     */
    public function doGetHtml()
    {
        global $_M;
        if (isset($_FILES['upfile'])) {
            $files = $_FILES['upfile'];
        }else{
            $this->error($_M['word']['dataerror']);
        }

        $path_info = pathinfo($files['name']);
        $ext = $path_info['extension'];
        if (!in_array($ext, $this->allow_ext)) {
            $this->error($_M['word']['dataerror']);
        }
        $cache_file = PATH_CACHE . "cahce_doc.{$ext}";
        $res = move_uploaded_file($files['tmp_name'], $cache_file);
        if (!$res) {
            $this->error($_M['word']['dataerror']);
        }

        $html = $this->docparse->parseDoc($cache_file);
        delfile($cache_file);

        if ($html !== false) {
            $this->success($html);
        }
        $this->error($_M['word']['dataerror']);
    }
}

# This program is an open source system, commercial use, please consciously to purchase commercial license.

