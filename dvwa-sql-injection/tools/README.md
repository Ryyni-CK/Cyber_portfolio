# tools/

Utilities for keeping writeups consistent.

## make_banner.py

Generates a GitHub-dark banner matching the house style.

```bash
pip install pillow
python tools/make_banner.py \
    --title "SQL Injection" \
    --subtitle "Union-based data extraction" \
    --payload "' UNION SELECT user,password-- -" \
    --tag "target: DVWA  ·  SQLi  ·  CWE-89" \
    --out images/banner.png
```

Run `python tools/make_banner.py -h` for all options. On non-Linux systems pass
`--fontdir` pointing to a folder with the DejaVu `.ttf` files if they aren't found automatically.
