import numpy as np, wave
from scipy.signal import lfilter
SR=44100
def mf(m): return 440*2**((m-69)/12)
def lp(x,fc): a=1-np.exp(-2*np.pi*fc/SR); return lfilter([a],[1,-(1-a)],x)
def music(dur,bpm,cuts,seed=3,end=12.0):
    rng=np.random.default_rng(seed); n=int(dur*SR); b=60/bpm; m=np.zeros(n)
    def add(sig,at,g=1):
        i=int(at*SR)
        if i<0 or i>=n: return
        j=min(n,i+len(sig)); m[i:j]+=sig[:j-i]*g
    def env(L,a,d): tt=np.arange(L)/SR; e=np.exp(-tt/d); k=max(1,int(a*SR)); e[:k]*=np.linspace(0,1,k); return e
    def kick():
        L=int(.30*SR); tt=np.arange(L)/SR; f=48+60*np.exp(-tt*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*env(L,.003,.12)
    def shaker(acc):
        L=int(.07*SR); x=rng.standard_normal(L); x=lp(x-lp(x,3000),9000); return x*env(L,.004,.025)*(1.6 if acc else 1)
    def bass(f,L=int(.5*SR)):
        tt=np.arange(L)/SR; return (np.sin(2*np.pi*f*tt)+.25*np.sin(4*np.pi*f*tt))*env(L,.01,.22)
    def pluck(f,L=int(.7*SR)):
        tt=np.arange(L)/SR; x=np.sin(2*np.pi*f*tt)+.4*np.sin(4*np.pi*f*tt)*np.exp(-tt*8)+.15*np.sin(6.0*np.pi*f*tt)*np.exp(-tt*14)
        return x*env(L,.004,.18)
    def rhodes(f,L):
        tt=np.arange(L)/SR; x=np.sin(2*np.pi*f*tt)+.35*np.sin(4*np.pi*f*tt+.5)*np.exp(-tt*2)
        x*=1+.08*np.sin(2*np.pi*4.5*tt); return x*np.minimum(1,tt/.04)*np.minimum(1,(L/SR-tt)/.25)*np.exp(-tt*.35)
    chords=[(57,[57,60,64]),(53,[53,57,60]),(48,[48,52,55]),(55,[55,59,62])]   # Am F C G
    motif=[ # (pulso dentro de 8 compases de 4 tiempos... 2 compases por acorde) (beat, midi)
      [(0,76),(1,74),(1.5,72),(3,69)],            # Am
      [(0,72),(1.5,69),(2,72),(3,76)],            # F
      [(0,79),(1,76),(2,74),(3,72)],              # C
      [(0,74),(1.5,71),(2,74),(3,71)]]            # G
    nb=int(dur/b)+1; bars=int(dur/(4*b))+1
    for bar in range(bars):
        root,ch=chords[bar%4]; t0=bar*4*b
        for f in ch: add(rhodes(mf(f+12),int(4*b*SR)),t0,.075)
        for bt,mid in motif[bar%4]: add(pluck(mf(mid)),t0+bt*b,.15)
        for bt in (0,1.5,2.5): add(bass(mf(root-12)),t0+bt*b,.5)
        for bt in (0,2,2.5): add(kick(),t0+bt*b,.42)
    for q in range(nb*2): add(shaker(q%2==1),q*b/2,.05)
    # acentos suaves en los cortes (campana corta)
    for c in cuts: add(pluck(mf(88),int(.9*SR)),c,.09)
    m=lp(m,7500)
    t=np.arange(n)/SR; m*=np.minimum(1,t/.4)*np.minimum(1,(dur-t)/1.4)
    return m
def save(path,x):
    w=wave.open(path,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
