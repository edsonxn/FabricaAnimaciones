import sys, json
sys.stdout.reconfigure(encoding='utf-8')
t = json.load(open('timeline.json', encoding='utf-8'))
for e in t['escenas']:
    if e['id'] != sys.argv[1]:
        continue
    print(f"== {e['id']}  {e['t0']:.1f}-{e['t1']:.1f}")
    for i, f in enumerate(e['frases']):
        ws = ' '.join(f"{w['w'].strip()}@{w['s']:.1f}" for w in f['words'])
        print(f"[{i}] {f['t0']:.1f}-{f['t1']:.1f}: {ws}")
