<!DOCTYPE html>
<html lang="ru">
    <head>
            <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, inital-scale=1.0">
        <title><?= "Переменные"; ?></title>
    </head>
    <body>
        <?php
            define("My_age", "21"); //Константа
            echo My_age . '<br>';

            $number = 5; //ineger
            $num = -0.55; //float
            $str = "Hello, world!"; //string
            $bool = false; //boolean

            $a = 0.5;
            $b = "0.5";

            echo $a + $b;

            echo $str . ": " . $number . ". Var 2: " . $num;
        ?>
    </body>
</html>