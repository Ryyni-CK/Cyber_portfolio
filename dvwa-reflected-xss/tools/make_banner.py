#!/usr/bin/env python3
"""
Generate a matching GitHub-dark banner for a writeup.

Example:
    python tools/make_banner.py \
        --title "SQL Injection" \
        --subtitle "Union-based data extraction" \
        --payload "' UNION SELECT user,password-- -" \
        --tag "target: DVWA  ·  SQLi  ·  CWE-89" \
        --out images/banner.png

Requires Pillow:  pip install pillow
Falls back to the DejaVu fonts shipped with most Linux distros; override with --fontdir.
"""
import argparse, os, sys
from PIL import Image, ImageDraw, ImageFont

BG, TXT, MUT = "#0d1117", "#e6edf3", "#8b949e"
GREEN, GREEN_D, BLUE = "#3fb950", "#238636", "#58a6ff"


def find_font(fontdir, filename):
    candidates = [fontdir] if fontdir else []
    candidates += [
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/dejavu",
        "/Library/Fonts", "/System/Library/Fonts",
        "C:/Windows/Fonts",
    ]
    for c in candidates:
        p = os.path.join(c, filename)
        if os.path.exists(p):
            return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kicker", default="WEB APPLICATION PENETRATION TEST  ·  WALKTHROUGH")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--payload", default="", help="mono chip shown bottom-left")
    ap.add_argument("--tag", default="", help="muted text bottom-right")
    ap.add_argument("--out", default="images/banner.png")
    ap.add_argument("--fontdir", default="")
    args = ap.parse_args()

    sans = find_font(args.fontdir, "DejaVuSans.ttf")
    sansb = find_font(args.fontdir, "DejaVuSans-Bold.ttf")
    mono = find_font(args.fontdir, "DejaVuSansMono.ttf")
    monob = find_font(args.fontdir, "DejaVuSansMono-Bold.ttf")
    if not all([sans, sansb, mono, monob]):
        sys.exit("Could not locate DejaVu fonts. Pass --fontdir pointing to a folder "
                 "containing DejaVuSans*.ttf / DejaVuSansMono*.ttf")

    def F(size, path):
        return ImageFont.truetype(path, size)

    W, H = 1200, 340
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=GREEN_D)
    for gx in range(0, W, 26):
        for gy in range(20, H, 26):
            d.point((gx, gy), fill="#11202a")

    d.text((60, 70), args.kicker, font=F(20, sansb), fill=GREEN, anchor="la")
    d.text((60, 104), args.title, font=F(64, sansb), fill=TXT, anchor="la")
    if args.subtitle:
        d.text((60, 176), args.subtitle, font=F(38, mono), fill=BLUE, anchor="la")

    if args.payload:
        cf = F(26, monob)
        tw = d.textlength(args.payload, font=cf)
        d.rounded_rectangle([60, 250, 60 + tw + 40, 300], 10, fill="#0b2f18",
                            outline=GREEN_D, width=2)
        d.text((80, 275), args.payload, font=cf, fill=GREEN, anchor="lm")

    if args.tag:
        d.text((W - 60, 285), args.tag, font=F(18, mono), fill=MUT, anchor="ra")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    img.save(args.out)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
