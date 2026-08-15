# Commands used

All run from the exercise's scanning box over SSH.

```bash
# 1) my own address
sudo ifconfig                              # eth0 -> inet 173.2.76.2 (subnet 173.2.76.0/24)

# 2) discover live hosts on the /29; find the one with MANY open ports
sudo nmap -F 173.2.76.0/29                 # -> crvekruh_meta2_1 (173.2.76.3)

# 3) enumerate open HIGH ports (fast, no version detection)
sudo nmap -p 1025-65535 -T4 173.2.76.3
#    -T5 is the "fastest" template the exercise specifies, but on a lossy path it
#    hits the retransmission cap ("giving up on port"); -T4 completes reliably.

# 4) version-detect ONLY the open ports (near-instant vs re-scanning 64k)
sudo nmap -p 1099,2959,3632,5900,6000,6697,8787,9897,19237,19324,19982,26088,27131,\
30176,40733,42461,45877,46857,57987,58014,<smtp>,62281,62466 -sV 173.2.76.3

# the exercise-spec single command (slower, all-in-one):
sudo nmap -p 1025-65535 -sV -T5 173.2.76.3
```

Answer: the line whose SERVICE is `smtp` (Postfix smtpd) — its port number is the submission (redacted here).
