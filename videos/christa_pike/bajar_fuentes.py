# -*- coding: utf-8 -*-
"""Baja el TEXTO completo de las fuentes (no resúmenes) a fuentes/*.txt para verificar cada dato del guion."""
import re, sys, json, pathlib, requests
from html.parser import HTMLParser

AQUI = pathlib.Path(__file__).parent
OUT = AQUI / "fuentes"
OUT.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}


class Tx(HTMLParser):
    def __init__(self):
        super().__init__()
        self.t, self.skip = [], 0

    def handle_starttag(self, tag, a):
        if tag in ("script", "style", "noscript", "svg", "nav", "footer", "header"):
            self.skip += 1
        if tag in ("p", "br", "h1", "h2", "h3", "li"):
            self.t.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg", "nav", "footer", "header"):
            self.skip = max(0, self.skip - 1)

    def handle_data(self, d):
        if not self.skip and d.strip():
            self.t.append(d.strip() + " ")


def texto(html):
    p = Tx()
    p.feed(html)
    s = "".join(p.t)
    return re.sub(r"\n\s*\n+", "\n\n", s)


FUENTES = {
    "wjhl": "https://www.wjhl.com/news/tennessee-prison-commissioner-resigns-after-failed-execution-of-christa-pike/",
    "abc7_ap": "https://abc7news.com/post/tennessees-prisons-chief-is-resigning-failed-execution-attempt-christa-pike/19904806/",
    "9news_ap": "https://www.9news.com/article/news/nation-world/tennessee-prison-chief-resigns-failed-execution-christa-pike/507-6c79184a-5e2c-4cc1-a520-96804be77e53",
    "newsweek": "https://www.newsweek.com/tennessee-prisons-chief-resigns-after-christa-pike-execution-failure-12520776",
    "fox9": "https://www.fox9.com/news/christa-pike-latest-tennessee-prisons-chief-resigns-after-failed-execution",
    "cbs": "https://www.cbsnews.com/amp/news/tennessee-christa-gail-pike-execution-woman-death-row",
    "aljazeera": "https://www.aljazeera.com/news/2026/10/3/tennessee-prisons-official-resigns-after-christa-pikes-failed-us-execution",
    "wapo": "https://www.washingtonpost.com/nation/2026/10/03/tennessee-prisons-chief-resigns-after-failed-christa-pike-execution-gov-says/",
}

if __name__ == "__main__":
    # Wikipedia por API (texto plano)
    for tit, nom in (("Christa_Pike", "wiki_christa_pike"), ("Murder_of_Colleen_Slemmer", "wiki_slemmer")):
        try:
            r = requests.get("https://en.wikipedia.org/w/api.php", headers=UA, timeout=30, params=dict(
                action="query", prop="extracts", explaintext=1, titles=tit, format="json", redirects=1))
            pg = list(r.json()["query"]["pages"].values())[0]
            (OUT / f"{nom}.txt").write_text(pg.get("extract", ""), encoding="utf-8")
            print(nom, len(pg.get("extract", "")))
        except Exception as e:
            print(nom, "ERROR", e)
    for k, u in FUENTES.items():
        try:
            r = requests.get(u, headers=UA, timeout=30)
            s = texto(r.text)
            (OUT / f"{k}.txt").write_text(f"URL: {u}\nHTTP {r.status_code}\n\n{s}", encoding="utf-8")
            print(k, r.status_code, len(s))
        except Exception as e:
            print(k, "ERROR", e)
