import numpy as np, sys, json, subprocess, wave
SR=44100
def make(dur,bpm,key_roots,sfx,music=True,seed=1):
    rng=np.random.default_rng(seed); n=int(dur*SR); t=np.arange(n)/SR
    mix=np.zeros(n); beat=60/bpm
    def add(buf,at,sig,g=1.0):
        i=int(at*SR); 
        if i>=n: return
        j=min(n,i+len(sig)); buf[i:j]+=sig[:j-i]*g
    def lp(x,a): 
        y=np.zeros_like(x); s=0
        for k in range(len(x)): s+=a*(x[k]-s); y[k]=s
        return y
    def env(L,a=.005,d=.2):
        e=np.exp(-np.arange(L)/SR/d); e[:int(a*SR)]*=np.linspace(0,1,int(a*SR)); return e
    def kick():
        L=int(.28*SR); tt=np.arange(L)/SR; f=45+110*np.exp(-tt*28); ph=2*np.pi*np.cumsum(f)/SR
        return np.sin(ph)*env(L,.002,.11)
    def hat():
        L=int(.06*SR); x=rng.standard_normal(L); x=x-np.concatenate([[0],x[:-1]]); return x*env(L,.001,.018)
    def clap():
        L=int(.18*SR); x=rng.standard_normal(L); x=lp(x,.35); return x*env(L,.002,.07)*2
    def bass(f,L):
        tt=np.arange(L)/SR; x=np.sin(2*np.pi*f*tt)+.3*np.sin(4*np.pi*f*tt); return x*env(L,.01,.28)
    def pluck(f,L=int(.35*SR)):
        tt=np.arange(L)/SR; x=np.sin(2*np.pi*f*tt)+.5*np.sin(4*np.pi*f*tt)*np.exp(-tt*9)+.25*np.sin(6*np.pi*f*tt)*np.exp(-tt*14)
        return x*env(L,.003,.12)
    def pad(f,L):
        tt=np.arange(L)/SR; x=sum(np.sin(2*np.pi*f*k*tt+k) for k in (1,1.005,2))/3; return x*np.minimum(1,tt/.3)*np.minimum(1,(L/SR-tt)/.3)
    if music:
        m=np.zeros(n); k=kick(); h=hat(); c=clap()
        nb=int(dur/beat)+1
        for b in range(nb):
            at=b*beat
            if at<.0: continue
            add(m,at,k,.9)
            add(m,at+beat/2,h,.35)
            if b%4 in(1,3) and at>3.9: add(m,at,c,.35)
        # bajo + arpegio + pad sobre progresión (1 acorde por compás de 4 pulsos)
        scale=[0,3,7,10,12,15,19]  # menor pentatónica extendida
        for bar in range(int(dur/(4*beat))+1):
            root=key_roots[bar%len(key_roots)]; at=bar*4*beat
            for q in range(8):  # corcheas de bajo
                add(m,at+q*beat/2,bass(root*(1 if q%4!=3 else 1.5 if False else 1),int(beat*.5*SR)),.55 if q%2==0 else .0)
            for q in range(8):
                f=root*4*2**(scale[[0,2,3,2,4,2,3,1][q]]/12)
                add(m,at+q*beat/2,pluck(f),.17)
            add(m,at,pad(root*2,int(4*beat*SR)),.12)
            add(m,at,pad(root*2*2**(7/12),int(4*beat*SR)),.09)
        # sidechain suave
        sc=np.ones(n)
        for b in range(nb):
            i=int(b*beat*SR); L=int(.18*SR)
            if i+L<n: sc[i:i+L]=np.minimum(sc[i:i+L],1-.55*np.exp(-np.arange(L)/SR/.07))
        m*=sc; mix+=m*0.8
    # SFX
    s=np.zeros(n)
    def whoosh(L=int(.45*SR),up=True):
        x=rng.standard_normal(L); tt=np.arange(L)/L; out=np.zeros(L); 
        y=lp(x,.08); y2=lp(x,.4); mixf=tt if up else 1-tt
        out=y*(1-mixf)+y2*mixf; return out*np.sin(np.pi*tt)**1.5*2.2
    def pop():
        L=int(.12*SR); tt=np.arange(L)/SR; return np.sin(2*np.pi*(480+220*np.exp(-tt*30))*tt)*env(L,.008,.05)
    def tick():
        L=int(.02*SR); return lp(rng.standard_normal(L),.25)*env(L,.001,.008)
    def thud():
        L=int(.5*SR); tt=np.arange(L)/SR; return np.sin(2*np.pi*(70*np.exp(-tt*3)+35)*tt)*env(L,.002,.2)*1.4
    def ding():
        L=int(1.0*SR); tt=np.arange(L)/SR; return (np.sin(2*np.pi*1318*tt)+.5*np.sin(2*np.pi*1975*tt))*env(L,.002,.4)*.6
    def impact():
        L=int(.9*SR); tt=np.arange(L)/SR; x=np.sin(2*np.pi*(55*np.exp(-tt*2.5)+30)*tt)*env(L,.001,.35); return x*1.3
    T={'whoosh':whoosh,'pop':pop,'tick':tick,'thud':thud,'ding':ding,'impact':impact}
    for typ,at in sfx:
        if typ in('whoosh','impact'): continue
        else: add(s,at,T[typ](),{'pop':.16,'tick':.05,'thud':.3,'ding':.22,'impact':0}[typ])
    mix+=s
    # fade out final
    mix*=np.minimum(1,(dur-t)/1.2)
    mix=mix/ (np.abs(mix).max()+1e-9)*.5
    return (mix*32767).astype(np.int16)
def save(path,x):
    w=wave.open(path,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes()); w.close()
