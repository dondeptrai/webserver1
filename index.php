<?php

$host = "localhost";  
$username = "root";   
$password = "";       
$dbname = "school";   

$conn = new mysqli($host, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Kết nối thất bại: " . $conn->connect_error);
}

$sql = "SELECT id, name, age, class FROM students";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    
    echo "<h2>Danh sách học sinh:</h2>";
    echo "<table border='1'>
            <tr>
                <th>ID</th>
                <th>Tên</th>
                <th>Tuổi</th>
                <th>Lớp</th>
            </tr>";
    while($row = $result->fetch_assoc()) {
        echo "<tr>
                <td>" . $row["id"] . "</td>
                <td>" . $row["name"] . "</td>
                <td>" . $row["age"] . "</td>
                <td>" . $row["class"] . "</td>
              </tr>";
    }
    echo "</table>";
} else {
    echo "Không có học sinh nào.";
}


$conn->close();
?>
