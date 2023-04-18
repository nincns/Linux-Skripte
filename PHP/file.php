<?php
$path = "./";
if (isset($_POST['delete_file'])) {
    $file_to_delete = $_POST['delete_file'];
    if (file_exists($file_to_delete)) {
        unlink($file_to_delete);
        echo "File successfully deleted.";
    } else {
        echo "File could not be deleted: File does not exist.";
    }
}
if (isset($_POST['create_dir'])) {
    $new_dir = $path . $_POST['new_dir'];
    if (!file_exists($new_dir)) {
        mkdir($new_dir);
        echo "Directory successfully created.";
    } else {
        echo "Directory could not be created: Directory already exists.";
    }
}
if (isset($_GET['dir'])) {
    $path = $_GET['dir'];
}
$dir_handle = opendir($path);
?>
<hr>
<div style="text-align: center;">
    <img src="logo.png" alt="Logo" width="400" height="400">
    <hr style='border-top: 1px solid #ccc;'>
</div>
<?php
echo "<table style='width:100%;'>";
echo "<colgroup><col style='width:25%'><col style='width:20%'><col style='width:20%'><col style='width:20%'><col style='width:15%'></colgroup>";
echo "<tr><th style='text-align:left;'>Name</th><th style='text-align:left;'>Size</th><th style='text-align:left;'>Created</th><th style='text-align:left;'>Modified</th><th style='text-align:left;'>Options</th></tr>";
$dirs = array();
$files = array();
while ($file = readdir($dir_handle)) {
    if ($file != "." && $file != "..") {
        $file_path = $path . $file;
        $file_size = filesize($file_path);
        $file_created = date("Y-m-d H:i:s", filectime($file_path));
        $file_modified = date("Y-m-d H:i:s", filemtime($file_path));
        if (is_dir($file_path) || !in_array(strtolower(pathinfo($file_path, PATHINFO_EXTENSION)), array('html', 'php', 'css'))) {
            if (is_dir($file_path)) {
                $dirs[] = "<tr><td><a href='?dir=$file_path/'>$file/</a></td><td>-</td><td>$file_created</td><td>$file_modified</td><td>-</td></tr>";
            } else {
                $files[] = "<tr><td><a href='$file_path'>$file</a></td><td>$file_size</td><td>$file_created</td><td>$file_modified</td><td><form style='display: inline-block;' method='post' onsubmit=\"return confirm('Are you sure you want to delete this file?')\"><input type='hidden' name='delete_file' value='$file_path'><input type='submit' value='Delete'></form></td></tr>";
            }
        }
    }
}
closedir($dir_handle);
sort($dirs);
foreach ($dirs as $dir) {
    echo $dir;
}
rsort($files);
foreach ($files as $file) {
    echo $file;
}
echo "<tr><td colspan='5' style='border-bottom: 1px solid #ccc;'></td></tr>";
echo "<tr><td colspan='5'>";
echo "<form enctype='multipart/form-data' action='' method='POST' style='display: inline-block; margin-right: 10px;'>";
echo "<input type='hidden' name='MAX_FILE_SIZE' value='1000000' />";
echo "<input type='file' name='userfile' />";
echo "<input type='submit' value='Upload File' />";
echo "</form>";
echo "<form method='POST' style='display: inline-block;'>";
echo "<input type='text' name='new_dir' placeholder='New Directory'>";
echo "<input type='submit' name='create_dir' value='Create Directory'>";
echo "</form>";
if(isset($_FILES['userfile'])) {
    $upload_file = $path . basename($_FILES['userfile']['name']);
    if (move_uploaded_file($_FILES['userfile']['tmp_name'], $upload_file)) {
        echo "File uploaded successfully.";
        header("Location: " . $_SERVER['REQUEST_URI'] . "&uploaded");
        exit;
    } else {
        echo "An error occurred while uploading the file.";
    }
}
if (isset($_POST['create_dir'])) {
    $new_dir = trim($_POST['new_dir']);
    if (empty($new_dir)) {
        echo "Please enter a directory name.";
    } else {
        $new_dir = rtrim($path, '/') . '/' . $new_dir;
        if (file_exists($new_dir) && is_dir($new_dir)) {
            echo "Directory could not be created: Directory already exists.";
        } else if (mkdir($new_dir, 0777)) {
            echo "Directory successfully created.";
            header("Location: " . $_SERVER['REQUEST_URI'] . "&created");
            exit;
        } else {
            echo "Error creating directory.";
        }
    }
}
echo "</td></tr>";
echo "</table>";