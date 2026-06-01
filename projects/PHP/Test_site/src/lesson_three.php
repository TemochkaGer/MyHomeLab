<!DOCTYPE html>
<html lang="ru">
    <head>
            <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, inital-scale=1.0">
        <title><?= "Работа со строками"; ?></title>
    </head>
    <body>
        <?php
            $str = "Hello";
            echo "VAR: " . $str . "<br>"; //На обработку "" требуется в два раза больше ОЗУ, чем для ''
            echo "<input type=\"text\">" . "<br>";

            $length = strlen($str); //Узнать длину строки
            echo $length . "<br>";
            $space = "     me     ";
            echo trim($space) . "<br>"; //Убрать из строки все пробелы

            echo md5($str); //Хэширование
        ?>
    </body>
</html>