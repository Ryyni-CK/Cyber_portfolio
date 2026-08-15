# payloads/

Minimal PHP files used in this walkthrough. For an authorized DVWA lab only.

- **ls.php** — `print_r(scandir("../"))`; run from `hackable/uploads/` it lists the
  parent `hackable/` directory to find the randomly-named flag file.
- **print.php** — `readfile("../<flag>.php")`; edit the filename to the one `ls.php`
  reveals, then upload and open with Ctrl+U to read the flag.
