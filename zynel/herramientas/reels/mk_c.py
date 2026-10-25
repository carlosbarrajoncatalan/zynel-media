import numpy as np, wave
from music import music
from audio import make, SR
def build(r,dur,pops,ticks,extra,cuts):
    sfx=[('pop',x) for x in pops]
    for a,b,st in ticks:
        x=a
        while x<b: sfx.append(('tick',x)); x+=st
    sfx+=extra
    s=make(dur,120,[55],sfx,False).astype(float)/32767     # solo efectos (pico .5)
    m=music(dur,100,cuts)
    m=m/np.abs(m).max()*0.40
    def sv(p,x):
        x=x/np.abs(x).max()*.9; w=wave.open(p,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
    sv(r+'_ms.wav',m+s*0.7)
    sv(r+'_sfx.wav',s)
build('r1c',15.6,(0.05,1.8,3.7,3.9,6.1,7.2,8.5,12.2),((3.8,5.5,.12),(6.2,7.4,.12)),[('thud',7.2),('ding',12.3)],[3.6,6.0,8.4,12.0])
build('r2c',15.6,(0.05,1.5,3.1,3.8,4.6,5.4,6.7,9.7,12.2),((6.8,8.8,.12),),[('ding',12.3)],[3.0,6.6,9.6,12.0])
