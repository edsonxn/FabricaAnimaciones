import sys,json;sys.path.insert(0,'flow/v3');import prompts as p
for i in sys.argv[1:]:
    t,ing=p.prompt(i); print('##',i,json.dumps(ing)); print(t)
