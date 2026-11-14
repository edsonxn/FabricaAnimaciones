import sys,glob,os
from PIL import Image, ImageDraw
fs=sorted(glob.glob(sys.argv[1]));tw=480;W=4
s=Image.new('RGB',(W*tw,((len(fs)+W-1)//W)*290))
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGB');im.thumbnail((tw,270));c=Image.new('RGB',(tw,290));c.paste(im);ImageDraw.Draw(c).text((4,272),os.path.basename(f),fill='yellow');s.paste(c,((i%W)*tw,(i//W)*290))
s.save(sys.argv[2],quality=80)
