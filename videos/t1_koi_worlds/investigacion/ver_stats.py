import json, os
D = os.path.dirname(os.path.abspath(__file__))
tot = {}
for g in ('115660540726095062', '115660540726095063'):
    d = json.load(open(os.path.join(D, 'stats_' + g + '.json'), encoding='utf-8'))
    for s, t in d['teams'].items():
        print(g[-2:], s, t['dragons'], 'torres', t['towers'])
        for p in t['players']:
            print('   ', p['name'], p['champ'], f"{p['k']}/{p['d']}/{p['a']}", p['gold'], p['dmgShare'], p['kp'])
            a = tot.setdefault(p['name'], [0, 0, 0])
            a[0] += p['k']; a[1] += p['d']; a[2] += p['a']
print({k: (v, round((v[0] + v[2]) / max(1, v[1]), 1)) for k, v in tot.items()})
