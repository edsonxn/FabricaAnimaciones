import sys,glob
from PIL import Image, ImageDraw
ids=sys.argv[2:]; rows=[]
for i in ids:
    fs=sorted(glob.glob(f'crudo/flow3_{i}_*'))
    ims=[Image.open(f).convert('RGB').resize((640,357)) for f in fs]
    r=Image.new('RGB',(1300,377),(20,20,20))
    for k,im in enumerate(ims[:2]): r.paste(im,(k*650,0))
    ImageDraw.Draw(r).text((4,360),i,fill='yellow'); rows.append(r)
s=Image.new('RGB',(1300,377*len(rows)))
for k,r in enumerate(rows): s.paste(r,(0,k*377))
s.save(sys.argv[1],quality=82)
