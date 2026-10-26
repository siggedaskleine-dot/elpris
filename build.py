# Skapar en sida per elområde (se1/ ... se4/) från index.html, för Google-synlighet.
# Kör: python3 build.py
import re
BASE = "https://siggedaskleine-dot.github.io/elpris/"
AREAS = {"SE1": "Luleå", "SE2": "Sundsvall", "SE3": "Stockholm", "SE4": "Malmö"}
src = open("index.html", encoding="utf-8").read()
urls = [BASE]
for code, city in AREAS.items():
    slug = code.lower()
    title = f"Elpris idag {code} {city} – billigaste timmen idag och imorgon"
    desc = f"Elpriset idag och imorgon i elområde {code} ({city}) timme för timme. Se när det är billigast att diska, tvätta och ladda elbilen."
    s = src.replace('<html lang="sv">', f'<html lang="sv" data-area="{code}">')
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s)
    s = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', s)
    s = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title}">', s)
    s = s.replace(f'<link rel="canonical" href="{BASE}">', f'<link rel="canonical" href="{BASE}{slug}/">')
    s = s.replace("<h1>När är elen billigast?</h1>", f"<h1>Elpris idag i {code} {city}</h1>")
    import os
    os.makedirs(slug, exist_ok=True)
    open(f"{slug}/index.html", "w", encoding="utf-8").write(s)
    urls.append(f"{BASE}{slug}/")
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc><changefreq>daily</changefreq></url>\n" for u in urls) + "</urlset>\n")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
