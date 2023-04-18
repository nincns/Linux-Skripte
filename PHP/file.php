<?php
$path = "./";

if (isset($_POST['delete_file'])) {
  $file_to_delete = $_POST['delete_file'];
  if (file_exists($file_to_delete)) {
    unlink($file_to_delete);
    echo "Datei erfolgreich gelöscht.";
  } else {
    echo "Datei konnte nicht gelöscht werden: Datei existiert nicht.";
  }
}

if (isset($_POST['create_dir'])) {
  $new_dir = $path . $_POST['new_dir'];
  if (!file_exists($new_dir)) {
    mkdir($new_dir);
    echo "Ordner erfolgreich erstellt.";
  } else {
    echo "Ordner konnte nicht erstellt werden: Ordner existiert bereits.";
  }
}

if (isset($_GET['dir'])) {
  $path = $_GET['dir'];
}

$dir_handle = opendir($path);

echo "<table style='width:100%;'>";
echo "<colgroup><col style='width:25%'><col style='width:20%'><col style='width:20%'><col style='width:20%'><col style='width:15%'></colgroup>";
echo "<tr><th style='text-align:left;'>Name</th><th style='text-align:left;'>Größe</th><th style='text-align:left;'>Erstellt</th><th style='text-align:left;'>Geändert</th><th style='text-align:left;'>Optionen</th></tr>";

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
        $files[] = "<tr><td><a href='$file_path'>$file</a></td><td>$file_size</td><td>$file_created</td><td>$file_modified</td><td><form style='display: inline-block;' method='post' onsubmit=\"return confirm('Sind Sie sicher, dass Sie diese Datei löschen möchten?')\"><input type='hidden' name='delete_file' value='$file_path'><input type='submit' value='Löschen'></form></td></tr>";
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
echo "<tr><td colspan='5'>"; // Beginn der Tabellenzelle für den Dateiupload

echo "<form enctype='multipart/form-data' action='' method='POST' style='display: inline-block; margin-right: 10px;'>";
echo "<input type='hidden' name='MAX_FILE_SIZE' value='1000000' />";
echo "<input type='file' name='userfile' />";
echo "<input type='submit' value='Datei hochladen' />";
echo "</form>";

echo "<form method='POST' style='display: inline-block;'>";
echo "<input type='text' name='new_dir' placeholder='Neuer Ordner'>";
echo "<input type='submit' name='create_dir' value='Ordner erstellen'>";
echo "</form>";

if(isset($_FILES['userfile'])) {
  $upload_file = $path . basename($_FILES['userfile']['name']);
  if (move_uploaded_file($_FILES['userfile']['tmp_name'], $upload_file)) {
    echo "Die Datei wurde erfolgreich hochgeladen.";
    header("Location: " . $_SERVER['REQUEST_URI'] . "&uploaded"); // Hinzufügen von GET-Parameter für die Aktualisierung der Seite
    exit;
  } else {
    echo "Es ist ein Fehler beim Hochladen der Datei aufgetreten.";
  }
}


if (isset($_POST['create_dir'])) {
  $new_dir = trim($_POST['new_dir']);
  if (empty($new_dir)) {
    echo "Geben Sie bitte einen Ordnernamen ein.";
  } else {
    $new_dir = rtrim($path, '/') . '/' . $new_dir;
    if (file_exists($new_dir) && is_dir($new_dir)) {
      echo "Ordner konnte nicht erstellt werden: Ordner existiert bereits.";
    } else if (mkdir($new_dir, 0777)) {
      echo "Ordner erfolgreich erstellt.";
      header("Location: " . $_SERVER['REQUEST_URI'] . "&created"); // Hinzufügen von GET-Parameter für die Aktualisierung der Seite
      exit;
    } else {
      echo "Fehler beim Erstellen des Ordners.";
    }
  }
}

echo "</td></tr>"; // Ende der Tabellenzelle für den Dateiupload
?>

</table>