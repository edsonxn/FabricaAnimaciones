import sys,re,html
for fn in sys.argv[1:]:
    s=open(fn,encoding='utf-8',errors='ignore').read()
    m=re.search(r'id="wiki-content-block"(.*)',s,re.S); s=m.group(1) if m else s
    s=re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S)
    s=re.sub(r'<br\s*/?>|</p>|</li>|</tr>|</h\d>','\n',s); s=re.sub(r'<[^>]+>','',s); s=html.unescape(s)
    s=re.sub(r'\n\s*\n+','\n',s)
    open(fn[:-5]+'.txt','w',encoding='utf-8').write(s)
