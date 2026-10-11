"""python _t.py escena [n] -> n instantes repartidos en la escena"""
import sys, json
t = json.load(open('timeline.json', encoding='utf-8'))
e = {x['id']: x for x in t['escenas']}[sys.argv[1]]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 9
print(' '.join(f"{e['t0'] + (0.04 + 0.92 * i / (n - 1)) * (e['t1'] - e['t0']):.2f}" for i in range(n)))
