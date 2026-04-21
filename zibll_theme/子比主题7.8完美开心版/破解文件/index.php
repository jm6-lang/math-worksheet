<?php
$url = $_SERVER['REQUEST_URI'];

function getRandom($length) {
	$characters = 'abcdefghijklmnopqrstuvwxyz1234567890';
	$randomString = '';
	for ($i = 0; $i < $length; $i++) {
		$index = rand(0, strlen($characters) - 1);
		$randomString .= $characters[$index];
	}
	return $randomString;
}
function generate_randstr($url) {
	$key = strrev(md5($url));
	$num1 = rand(70,99);
	$num1r = strrev(strval($num1));
	$num2 = rand(70,99);
	$num2r = strrev(strval($num2));
	$key = substr($key,23).substr($key,0,23);
	$keystr = substr_replace($key,getRandom(3),$num1-69,0);
	$randstr = getRandom(3).$num1r.getRandom(rand(5,10)).$keystr.getRandom(100-$num2).$num2r;
	return $randstr;
}

header('Content-Type: application/json; charset=UTF-8');

if(strpos($url, '/api/auth') !== false){
	$time = time();
	$token = md5(uniqid(mt_rand(), true) . microtime());
	$randstr = generate_randstr($_POST['url']);
	$sign = md5($randstr.$time.$token.'ok');
    $data = ['error'=>true, 'error_code'=>0, 'msg'=>'', 'time'=>$time, 'token'=>$token, 'randstr'=>$randstr, 'code'=>base64_encode('恭喜您，授权验证成功'), 'sign'=>$sign];
    echo json_encode($data);
}
elseif(strpos($url, '/api/update') !== false){
    $version = $_POST['version'];
    $data = ['result'=>false, 'aut_error'=>false, 'msg'=>'暂无更新，您当前的版本已是最新版', 'version'=>$version];
    echo serialize($data);
}
