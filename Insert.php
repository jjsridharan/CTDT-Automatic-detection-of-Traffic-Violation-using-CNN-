<?php
    $mysql_host="localhost";
    $mysql_user="";
    $mysql_pass="";
    $mysql_db="";
    $con=@mysqli_connect($mysql_host,$mysql_user,$mysql_pass) or die("Error");
    mysqli_select_db($con,$mysql_db);
    $user=$_POST['name'];
    $licno=$_POST['licno'];
    $amount=$_POST['amount'];
    $qry="Insert into User values('$user','$licno','$amount')";
    $r=mysqli_query($con,$qry);
    if($r)
    {
        echo "Successfully Inserted";
    }
    else
    {
        echo "Error";
    }
?>