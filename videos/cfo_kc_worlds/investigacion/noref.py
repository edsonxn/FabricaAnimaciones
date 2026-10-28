import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
t = re.sub(r"<ref[^>]*/>", "", t); t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
sys.stdout.reconfigure(encoding="utf-8")
print(t)
