import sys,glob
from PIL import Image, ImageDraw
out=sys.argv[1]; ids=sys.argv[2:]; tw,th=400,223; W=2
rows=(len(ids)+W-1)//W
s=Image.new('RGB',(W*(2*tw+30),rows*(th+18)),(15,15,15)); d=ImageDraw.Draw(s)
for n,i in enumerate(ids):
    x=(n%W)*(2*tw+30); y=(n//W)*(th+18)
    for k,f in enumerate(sorted(glob.glob(f'crudo/flow3_{i}_*'))[:2]):
        s.paste(Image.open(f).convert('RGB').resize((tw,th)),(x+k*(tw+4),y))
    d.text((x+2,y+th+2),f'{i}  (izq=1, der=2)',fill='yellow')
s.save(out,quality=80)
