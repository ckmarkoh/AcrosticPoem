<?php

function get_client_ip() {
    $ipaddress = '';
    if (getenv('HTTP_CLIENT_IP'))
        $ipaddress = getenv('HTTP_CLIENT_IP');
    else if(getenv('HTTP_X_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_X_FORWARDED_FOR');
    else if(getenv('HTTP_X_FORWARDED'))
        $ipaddress = getenv('HTTP_X_FORWARDED');
    else if(getenv('HTTP_FORWARDED_FOR'))
        $ipaddress = getenv('HTTP_FORWARDED_FOR');
    else if(getenv('HTTP_FORWARDED'))
       $ipaddress = getenv('HTTP_FORWARDED');
    else if(getenv('REMOTE_ADDR'))
        $ipaddress = getenv('REMOTE_ADDR');
    else
        $ipaddress = 'UNKNOWN';
    return $ipaddress;
}
$t=time();
error_log('time:'.$t.',ip:'.get_client_ip().'\n', 3, "php_log.log");

if(isset($_POST['input_str'])){
	$input_str = $_POST['input_str'];
	$length = $_POST['length'];
	$position = $_POST['position'];
	$error = "";
	if(!isset($_POST['length'])){
		$error .= "Missing argument 'length'. ";
	}
	if(!isset($_POST['position'])){
		$error .= "Missing argument 'position'. ";
	}
	if(!preg_match("/^[\x{4e00}-\x{9fa5}]+$/u", $input_str)){
		$error .= "Invalid character. ";
	}
	if(mb_strlen($input_str,'utf-8') > 12){
		$error .= "Input string too long. ";
	}
	if($length !=5 && $length != 7 ){
		$error .= "Invalid length. ";
	}
    if( $position != "lr" && $position != "rl"  && $position > $length){
        $error .= "Invalid position. ";
    }
	if($error != ""){
		echo json_encode(array("error"=>$error));
	}
	else{
		
		$input_str_arg = "$input_str -l $length -p $position";
		error_log('time:'.$t.',ip:'.get_client_ip().',str:'.$input_str_arg.'\n', 3, "php_log.log");
		exec("python ./command.py $input_str_arg",$my_output);
		echo json_encode($my_output);
	}
}
?>
