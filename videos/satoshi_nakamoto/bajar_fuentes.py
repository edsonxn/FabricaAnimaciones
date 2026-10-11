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


WIKI = {
    "Satoshi_Nakamoto": "wiki_satoshi", "Adam_Back": "wiki_adam_back", "Hal_Finney_(computer_scientist)": "wiki_hal_finney",
    "Nick_Szabo": "wiki_nick_szabo", "Dorian_Nakamoto": "wiki_dorian", "Craig_Steven_Wright": "wiki_craig_wright",
    "Len_Sassaman": "wiki_sassaman", "Money_Electric:_The_Bitcoin_Mystery": "wiki_money_electric", "Hashcash": "wiki_hashcash",
    "Bitcoin": "wiki_bitcoin", "Genesis_block": "wiki_genesis", "History_of_bitcoin": "wiki_historia_bitcoin",
    "Bitcoin_Pizza_Day": "wiki_pizza", "Peter_Todd_(cryptographer)": "wiki_peter_todd", "Gavin_Andresen": "wiki_gavin",
    "Wei_Dai": "wiki_wei_dai", "Bit_gold": "wiki_bit_gold", "The_Mysterious_Mr._Nakamoto": "wiki_mysterious_mr",
    "Paul_Le_Roux": "wiki_le_roux", "Cypherpunk": "wiki_cypherpunk",
}

FUENTES = {
    "techcrunch_back": "https://techcrunch.com/2026/04/08/british-cryptographer-adam-back-denies-nyt-report-that-he-is-bitcoin-creator-satoshi-nakamoto/",
    "boingboing_nyt": "https://boingboing.net/2026/04/10/nyt-investigation-names-adam-back-as-bitcoins-satoshi-nakamoto.html",
    "financefeeds_2026": "https://financefeeds.com/satoshi-nakamoto-identity-2026-suspects-and-the-85b-question/",
    "forbes_armstrong": "https://www.forbes.com/sites/digital-assets/2026/03/26/who-is-satoshi-nakamoto-coinbase-ceo-reveals-he-now-thinks-he-knows-the-answer-to-the-massive-bitcoin-mystery/",
    "bstandard_back": "https://www.business-standard.com/markets/cryptocurrency/who-is-adam-back-the-bitcoin-pioneer-behind-blockstream-and-liquid-126100100684_1.html",
    "cryptotimes_leroux": "https://cryptotimes.io/2026/09/28/is-paul-le-roux-really-satoshi-nakamoto-what-the-record-actually-shows",
    "coin360_nyt": "https://coin360.com/news/adam-back-satoshi-nakamoto-nyt-investigation",
    "lopp_finney": "https://blog.lopp.net/was-satoshi-nakamoto-hal-finney/",
    "copa_judgment": "https://www.judiciary.uk/judgments/cryptoopen-patent-alliance-v-wright/",
    "bitcoin_whitepaper_wiki": "https://en.bitcoin.it/wiki/Bitcoin_white_paper",
    "genesis_bitcoinwiki": "https://en.bitcoin.it/wiki/Genesis_block",
}

if __name__ == "__main__":
    solo = sys.argv[1:]
    for tit, nom in WIKI.items():
        if solo and nom not in solo:
            continue
        try:
            r = requests.get("https://en.wikipedia.org/w/api.php", headers=UA, timeout=30, params=dict(
                action="query", prop="extracts", explaintext=1, titles=tit, format="json", redirects=1))
            pg = list(r.json()["query"]["pages"].values())[0]
            (OUT / f"{nom}.txt").write_text(pg.get("extract", ""), encoding="utf-8")
            print(nom, len(pg.get("extract", "")))
        except Exception as e:
            print(nom, "ERROR", e)
    for k, u in FUENTES.items():
        if solo and k not in solo:
            continue
        try:
            r = requests.get(u, headers=UA, timeout=30)
            s = texto(r.text)
            (OUT / f"{k}.txt").write_text(f"URL: {u}\nHTTP {r.status_code}\n\n{s}", encoding="utf-8")
            print(k, r.status_code, len(s))
        except Exception as e:
            print(k, "ERROR", e)
