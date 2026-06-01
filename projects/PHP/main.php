<?php

function truncate(string $string, int $length)
{
    return (string) substr($string, 0, $length) . "...";
}

print_r(truncate("Hello", 3));