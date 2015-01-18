<?php
require_once("./dbinfo.php");
//db connection
try {
    $db = new PDO("mysql:hostname=$hostname;dbname=$dbname", $dbusername, $dbpassword);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); // set the PDO to throw exception
}
catch(PDOException $e){
    echo "Coundn't connect to DB";
    die();
}

//usage of this update.php   update?number="..."&x="...."&method="...."&data="....."

if(isset($_GET['number']) && ($_GET['method'] == "isfinished")){
    //check if three fields are filled out
    $phoneNum = $_GET['number'];
    $pre = $db->prepare("SELECT * FROM delivery WHERE phoneNum=:phoneNum");
    $pre->execute(array(":phoneNum"=>"$phoneNum"));
    $row = $pre->fetch();
    if(isset($row['store']) && isset($row['address']) && isset($row['items'])){
        //return the json object
        $store = $row['store'];
        $address = $row['address'];
        $items = $row['items'];
        $jsonArr = array("address"=>"$address","store"=>"$store","items"=>"$items");
        echo json_encode($jsonArr);
        //delete the record
    }
    else{
        echo 0;
    }
}

else{
    //method must be update
    $phoneNum = $_GET['number'];
    try{
        //see if number doesn't exist
        $pre = $db->prepare("INSERT INTO delivery (phoneNum) VALUES (:phoneNum)");
        $pre->execute(array(":phoneNum"=>"$phoneNum"));
        echo "Inserted the record";

        //check what method is executed
        $method = $_GET['method'];
        if($method == "update"){
            $x = $_GET['x'];
            $data = $_GET['data'];
            if($x=="address"){
                //update address
                $pre2 = $db->prepare("UPDATE delivery SET address=:address WHERE phoneNum = :phoneNum");
                $pre2->execute(array(":address"=>"$data",":phoneNum"=>"$phoneNum"));
            }
            elseif($x=="store"){
                //update store
                $pre2 = $db->prepare("UPDATE delivery SET store=:store WHERE phoneNum = :phoneNum");
                $pre2->execute(array(":store"=>"$data",":phoneNum"=>"$phoneNum"));
            }
            elseif($x=="items"){
                //update items
                $pre2 = $db->prepare("UPDATE delivery SET items=:items WHERE phoneNum = :phoneNum");
                $pre2->execute(array(":items"=>"$data",":phoneNum"=>"$phoneNum"));
            }
            else{
                echo "wrong x variable";
                die();
            }
        }
        else{
            echo "wrong method";
            die();
        }
    }
    catch(PDOException $e){
        //if the number exist update them
        $x = $_GET['x'];
        $data = $_GET['data'];
        if($x=="address"){
            //update address
            $pre2 = $db->prepare("UPDATE delivery SET address=:address WHERE phoneNum = :phoneNum");
            $pre2->execute(array(":address"=>"$data",":phoneNum"=>"$phoneNum"));
        }
        elseif($x=="store"){
            //update store
            $pre2 = $db->prepare("UPDATE delivery SET store=:store WHERE phoneNum = :phoneNum");
            $pre2->execute(array(":store"=>"$data",":phoneNum"=>"$phoneNum"));
        }
        elseif($x=="items"){
            //update items
            $pre2 = $db->prepare("UPDATE delivery SET items=:items WHERE phoneNum = :phoneNum");
            $pre2->execute(array(":items"=>"$data",":phoneNum"=>"$phoneNum"));
        }
        else{
            echo "wrong x variable";
            die();
        }
    }
}
?>