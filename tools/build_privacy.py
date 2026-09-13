#!/usr/bin/env python3
"""Bygger om privacy.html för siboai.app ur app-repots policy.

Syfte: policyn på sajten och docs/PRIVACY-POLICY.md i app-repot får inte glida
ifrån varandra. Det här skriptet är den enda kopplingen mellan dem.

VIKTIGT: skriptet skriver BARA privacy.html. index.html, styles.css, support.html
och 404.html är handskrivna och rörs inte — en tidigare version av det här
skriptet genererade hela sajten och skulle ha skrivit över designsystemet.

HÅRDA KRAV: ingen analytics, inga cookies, inga tredjepartsresurser (inget CDN,
inga externa typsnitt, ingen JS). Platshållare ([ATT FYLLA I]) renderas synliga —
en policy med ofyllda fält ska se ofylld ut, inte se färdig ut.

Kör:  python3 tools/build_privacy.py
"""
import html
import io
import os
import re
import sys

SRC = os.path.expanduser("~/Projects/sibo-coach")       # app-repot (källan)
OUT = os.path.expanduser("~/Projects/sibo-ai-site")     # sajtrepot (målet)
KLOCKA = "SIBO AI"
ANSVARIG = "Menudo Consulting AB"
UPPDATERAD = "12 september 2026"
POLICY = f"{SRC}/docs/PRIVACY-POLICY.md"
TARGET = f"{OUT}/privacy.html"

HEAD = """<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#0e120d">
<link rel="canonical" href="https://siboai.app/privacy.html">
<link rel="icon" href="/img/favicon-64.png" sizes="64x64">
<link rel="icon" href="/img/icon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:url" content="https://siboai.app/privacy.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://siboai.app/img/og.jpg">
<link rel="stylesheet" href="/styles.css">
</head>
<body>

<header class="site"><div class="wrap">
  <a class="brand" href="/"><img src="/img/icon-192.png" alt="">SIBO AI</a>
  <nav>
    <a href="/#analys">Analysen</a>
    <a href="/#coachen">Coachen</a>
    <a href="/#integritet">Integritet</a>
    <a href="/#pris">Pris</a>
    <a href="/#faq">Frågor</a>
  </nav>
  <a class="btn btn-primary btn-sm" href="/support.html">Support</a>
</div></header>

<main>
<section>
  <div class="wrap doc">
"""

FOOT = """
  </div>
</section>
</main>

<footer class="site"><div class="wrap">
  <div class="foot-grid">
    <div>
      <h4>Produkten</h4>
      <a href="/#analys">Analysen</a>
      <a href="/#coachen">AI-coachen</a>
      <a href="/#pris">Pris</a>
      <a href="/#faq">Vanliga frågor</a>
    </div>
    <div>
      <h4>Integritet</h4>
      <a href="/privacy.html">Integritetspolicy</a>
      <a href="/support.html">Radera mina uppgifter</a>
    </div>
    <div>
      <h4>Support</h4>
      <a href="/support.html">Kontakta oss</a>
      <a href="/support.html">Hantera prenumeration</a>
      <a href="/support.html">Statistiken jag ser</a>
    </div>
    <div>
      <h4>Om</h4>
      <a href="/support.html">Menudo Consulting AB</a>
    </div>
  </div>
  <div class="foot-bar">
    <p>SIBO AI — Menudo Consulting AB.</p>
    <p>Den här webbplatsen använder inga cookies, ingen spårning, inga tredjepartsresurser och ingen JavaScript.</p>
  </div>
</div></footer>

</body>
</html>
"""


def md_to_html(md):
    """Minimal markdown: rubriker, listor, tabeller, fetstil, kod, länkar, ATT-markeringar."""
    lines = md.split("\n")
    out, in_list, in_ol, in_table = [], False, False, False

    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
        t = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', t)
        t = re.sub(r"\[ATT ([^\]]+)\]", r'<span class="todo">ATT \1</span>', t)
        return t

    def close():
        nonlocal in_list, in_ol, in_table
        if in_list:
            out.append("</ul>"); in_list = False
        if in_ol:
            out.append("</ol>"); in_ol = False
        if in_table:
            out.append("</table>"); in_table = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            close()
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            close()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            continue
        if re.match(r"^\|[\s:\-|]+\|$", line):
            continue                                  # tabellavskiljare
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not in_table:
                close()
                out.append("<table>")
                out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
                in_table = True
            else:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            continue
        if in_table:
            close()
        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            if not in_list:
                close()
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue
        m = re.match(r"^\d+\.\s+(.*)$", line)
        if m:
            if not in_ol:
                close()
                out.append("<ol>"); in_ol = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue
        if line.startswith("---"):
            close()
            out.append("<hr>")
            continue
        close()
        out.append(f"<p>{inline(line)}</p>")
    close()
    return "\n".join(out)


def main():
    if not os.path.isfile(POLICY):
        sys.exit(f"Källfilen saknas: {POLICY}")

    policy_md = io.open(POLICY, encoding="utf-8").read()

    # Dela i engelska / svenska på PART A / DEL B
    parts = re.split(r"^#+\s*(PART A|DEL B)\b.*$", policy_md, flags=re.M)
    if len(parts) >= 5:
        en_md, sv_md = parts[2], parts[4]
    else:
        en_md, sv_md = policy_md, ""

    body = [
        '<p class="eyebrow">Juridik</p>',
        "<h1>Privacy policy / Integritetspolicy</h1>",
        f'<p class="lede">{KLOCKA} · {ANSVARIG} · Senast uppdaterad {UPPDATERAD}</p>',
        '<p><a href="#en">English</a> · <a href="#sv">Svenska</a></p>',
        "<hr>",
        '<h2 id="en">Privacy policy (English)</h2>',
        md_to_html(en_md) if en_md.strip() else "<p>[engelska saknas i källfilen]</p>",
        "<hr>",
        '<h2 id="sv">Integritetspolicy (svenska)</h2>',
        md_to_html(sv_md) if sv_md.strip() else "<p>[svenska saknas i källfilen]</p>",
    ]

    doc = (HEAD.format(
        title=f"Integritetspolicy — {KLOCKA}",
        desc=f"Integritetspolicy för {KLOCKA}: vad som stannar på din enhet och vad som lämnar den.",
    ) + "\n".join(body) + FOOT)

    io.open(TARGET, "w", encoding="utf-8").write(doc)

    todo = doc.count('class="todo"')
    print(f"skrev {TARGET}")
    print(f"  {len(doc)} tecken · {todo} ofyllda ATT-markeringar")
    print("  index.html, styles.css, support.html och 404.html rördes inte.")


if __name__ == "__main__":
    main()
