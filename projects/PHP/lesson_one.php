<?php

$name = 'Brienna';

// BEGIN (write your solution here)
$new_name = "";

for ($i = strlen($name) -1; $i > -1; $i -= 1){
    $new_name .= $name[$i];
}

print_r($new_name);
// END