<?php
# MetInfo Enterprise Content Management System 
 

defined('IN_MET') or exit('No permission');

load::mod_class('user/web/class/other');

class qq extends other {

    public function __construct() {
        global $_M;
        if(!$_M['config']['met_qq_open']){
            okinfo($_M['url']['login'], $_M['word']['userqqclose']);
        }
        $this->appid = $_M['config']['met_qq_appid'];
        $this->appkey = $_M['config']['met_qq_appsecret'];
        $this->table = $_M['table']['user_other'];
        $this->type = 'qq';
    }

    public function get_login_url(){
        global $_M;

        $redirect_uri = $_M['url']['web_site'].'member/login.php?a=doother_login&type=qq';
        $url = "https://graph.qq.com/oauth2.0/authorize?";
        $url .= "client_id={$this->appid}";
        $url .= "&redirect_uri=".urlencode($redirect_uri);
        $url .= "&response_type=code";
        $url .= "&scope=get_user_info";
        $url .= "&state=".$this->get_state();
        return $url;
    }

    public function get_access_token_by_curl($code){
        global $_M;
        $redirect_uri = $_M['url']['web_site'].'member/login.php?a=doother_login&type=qq';
        $url = "https://graph.qq.com/oauth2.0/token";
        $send['code'] = $code;
        $send['client_id'] = $this->appid;
        $send['client_secret'] = $this->appkey;
        $send['grant_type'] = 'authorization_code';
        $send['fmt'] = 'json';
        $send['redirect_uri'] = $redirect_uri;
        $result = load::mod_class('user/web/class/curl_ssl', 'new')->curl_post($url, $send);
        $data = json_decode($result, true);
        if (!isset($data['access_token'])) {
            return false;
        }

        //
        $url = "https://graph.qq.com/oauth2.0/me";
        $send = array();
        $send['access_token'] = $data['access_token'];
        $send['fmt'] = 'json';
        $result = load::mod_class('user/web/class/curl_ssl', 'new')->curl_post($url, $send);
        $result = json_decode($result, true);

        if (!$result['openid']) {
            return false;
        }

        $redata = array();
        $redata['openid'] = $result['openid'];
        $redata['access_token'] = $data['access_token'];

        return $redata;
    }

    public function get_info_by_curl($unionid){
        global $_M;
        $data = $this->get_other_user($unionid);
        $url = "https://graph.qq.com/user/get_user_info";
        $send['access_token'] = $data['access_token'];
        $send['oauth_consumer_key'] = $this->appid;
        $send['openid'] = $data['openid'];
        $result = load::mod_class('user/web/class/curl_ssl', 'new')->curl_post($url, $send, 'get');
        $data = json_decode($result,true);

        if (!isset($data['ret']) || $data['ret']!==0) {
            return false;
        }

        $redata = array();
        $redata['username'] = $data['nickname'];
        $redata['user_img'] = '';
        return $redata;
    }

    public function error_curl($data){
    }
}


# This program is an open source system, commercial use, please consciously to purchase commercial license.

?>