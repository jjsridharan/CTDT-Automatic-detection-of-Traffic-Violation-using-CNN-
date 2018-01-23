<?php
    $mysql_host="localhost";
    $mysql_user="";
    $mysql_pass="";
    $mysql_db="";
    $con=@mysqli_connect($mysql_host,$mysql_user,$mysql_pass) or die("Error in executing");
    mysqli_select_db($con,$mysql_db) or die("Error in executing");
    $licno=$_POST['license'];
    $qry="Select * from User where licenseplate='$licno'";
    echo $qry;
    $r=mysqli_query($con,$qry);
    if($r)
    {
    $row=mysqli_fetch_assoc($r);
    $amount=$row['amount'];
    $amount-=100;
    $qry="Update User set amount='$amount' where licenseplate='$licno'";
    $r=mysqli_query($con,$qry);
    if($r)
    {
        echo "Successfully Executed";
    }
    else
    {
        echo "Error in executing";
    }
    }
    else
    {
        echo "Error in Execting";
    }
    
    
?>