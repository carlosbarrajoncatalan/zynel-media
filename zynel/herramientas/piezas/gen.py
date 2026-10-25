import asyncio, os, sys
from playwright.async_api import async_playwright
NAVY="#0B2B3E"
BG={"coral":("#F26363","sq_coral.png","#0B2B3E"),"off":("#F2EBEC","sq_off.png","#F26363"),"teal":("#5EBFB5","sq_teal.png","#0B2B3E"),"yel":("#F2A71B","sq_yellow.png","#0B2B3E")}
ICON={
"unlock":'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>',
"refresh":'<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.5 9a9 9 0 0 1 14.9-3.4L23 10M1 14l4.6 4.4A9 9 0 0 0 20.5 15"/>',
"db":'<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.7-4 3-9 3s-9-1.3-9-3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/>',
"key":'<circle cx="7.5" cy="15.5" r="5.5"/><path d="M11.4 11.6 21 2"/><path d="M15.5 7.5l3 3L22 7l-3-3"/>',
"shield":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
"drop":'<path d="M12 2.7C8 8 5 11.5 5 15a7 7 0 0 0 14 0c0-3.5-3-7-7-12.3z"/>',
"type":'<polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/>',
"chat":'<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.5 8.5 0 0 1-3.8-.9L3 21l1.9-5.1A8.4 8.4 0 0 1 3.9 11.5 8.5 8.5 0 0 1 12.4 3 8.4 8.4 0 0 1 21 11.5z"/>',
"layout":'<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/>',
}
CSS="""@font-face{font-family:SG;src:url(sg.ttf);font-weight:300 700}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:%(bg)s;font-family:SG,sans-serif;color:#0B2B3E;position:relative;overflow:hidden}
h1{position:absolute;left:84px;width:930px;font-weight:700;letter-spacing:-.01em;line-height:1.3}
h1 .hl{background:#0B2B3E;color:#F2EBEC;padding:.04em .2em .1em;border-radius:14px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.card{position:absolute;left:84px;width:912px;border-radius:38px;overflow:hidden}
.card img{width:100%%;height:100%%;display:block}
.p{position:absolute;left:84px;width:880px;font-size:46px;line-height:1.5}
.num{position:absolute;left:84px;top:96px;font-size:190px;font-weight:700;line-height:1;color:%(numc)s;letter-spacing:-.03em}
.ico{position:absolute;right:84px;top:116px;width:150px;height:150px;border-radius:36px;background:#0B2B3E;display:flex;align-items:center;justify-content:center}
.ico svg{width:84px;height:84px;fill:none;stroke:#F2EBEC;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.foot.l span,.cnt.l{color:rgba(242,235,236,.92)}
.chip{position:absolute;left:84px;font-size:32px;font-weight:700;background:#0B2B3E;color:#F2EBEC;padding:16px 30px 20px;border-radius:999px}
.foot{position:absolute;left:84px;bottom:56px;display:flex;align-items:center;gap:22px}
.foot img{width:68px;height:68px}
.foot span{font-size:22px;font-weight:700;letter-spacing:.17em;color:rgba(11,43,62,.72)}
.cnt{position:absolute;right:84px;bottom:76px;font-size:26px;font-weight:700;color:rgba(11,43,62,.72);letter-spacing:.08em}
"""
def page(kind,bgk,i,n,d):
    bg,logo,numc=BG[bgk]
    h=f"<style>{CSS%dict(bg=bg,numc=numc)}</style>"
    foot=f'<div class="foot"><img src="{logo}"><span>RRSS | WEB | MARKETING | IA</span></div><div class="cnt">{i}/{n}{" →" if i<n else ""}</div>'
    if kind=="cover":
        b=f'<h1 style="top:112px;font-size:76px">{d["h1"]}</h1><div class="card" style="left:{d.get("cl",84)}px;width:{d.get("cw",912)}px;border-radius:{d.get("cr",38)}px;top:{d.get("ctop",430)}px;height:{d.get("ch",590)}px;background:{d["cardbg"]}"><img src="{d["img"]}" style="object-fit:{d.get("fit","contain")}"></div><div class="p" style="top:{d.get("ptop",1062)}px;font-size:36px">{d["p"]}</div>'
    elif kind=="item":
        b=f'<div class="num">{d["num"]}</div><div class="ico"><svg viewBox="0 0 24 24">{ICON[d["icon"]]}</svg></div><h1 style="top:470px;font-size:88px">{d["h1"]}</h1><div class="p" style="top:{d.get("ptop",(740 if len(d["h1"])>20 else 640))}px">{d["p"]}</div><div class="chip" style="top:{d.get("ptop",(740 if len(d["h1"])>20 else 640))+250}px">{d["chip"]}</div>'
    elif kind=="statement":
        b=f'<h1 style="top:250px;font-size:100px">{d["h1"]}</h1><div class="p" style="top:{d.get("ptop",800)}px">{d["p"]}</div>'
    elif kind=="photo":
        b=f'<h1 style="top:112px;font-size:70px">{d["h1"]}</h1><div class="card" style="top:{d.get("ctop",400)}px;height:{d.get("ch",640)}px;background:{d.get("cardbg","#fff")}"><img src="{d["img"]}" style="object-fit:{d.get("fit","cover")}"></div><div class="p" style="top:{d.get("ptop",1080)}px;font-size:34px">{d["p"]}</div>'
    elif kind=="bleed":
        b=f'<div style="position:absolute;inset:0;background:url({d["img"]}) {d.get("pos","70%")} center/cover no-repeat"></div><div style="position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(rgba(11,43,62,.9),rgba(11,43,62,.72) 58%,rgba(11,43,62,0))"></div><div style="position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(rgba(11,43,62,0),rgba(11,43,62,.6))"></div><h1 style="top:112px;font-size:92px;color:#F2EBEC">{d["h1"]}</h1><div class="p" style="top:{d.get("ptop",372)}px;font-size:40px;color:#F2EBEC">{d["p"]}</div>'
        foot=foot.replace('class="foot"','class="foot l"').replace('class="cnt"','class="cnt l"')
    elif kind=="fullimg":
        b=f'<img src="{d["img"]}" style="position:absolute;left:{d.get("ix",80)}px;top:{d.get("iy",390)}px;width:{d.get("iw",920)}px"><h1 style="top:112px;font-size:{d.get("hs",84)}px">{d["h1"]}</h1><div class="p" style="top:{d.get("ptop",345)}px;font-size:38px">{d["p"]}</div>'
    elif kind=="recap":
        ic="".join(f'<div style="width:190px;text-align:center"><div style="width:190px;height:190px;border-radius:44px;background:#0B2B3E;display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 24 24" style="width:100px;height:100px;fill:none;stroke:#F2EBEC;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round">{ICON[k]}</svg></div><div style="margin-top:20px;font-size:30px;font-weight:700">{t}</div></div>' for k,t in d["icons"])
        b=f'<h1 style="top:160px;font-size:104px">{d["h1"]}</h1><div style="position:absolute;left:84px;top:690px;width:912px;display:flex;justify-content:space-between">{ic}</div><div class="p" style="top:1020px;font-size:42px">{d["p"]}</div>'
    elif kind=="question":
        b=f'<h1 style="top:112px;font-size:84px">{d["h1"]}</h1><div class="card" style="top:480px;height:520px;background:{d["cardbg"]}"><img src="{d["img"]}" style="object-fit:{d.get("fit","contain")}"></div><div class="p" style="top:1040px;font-size:38px">{d["p"]}</div>'
    return f'<!doctype html><html><head><meta charset="utf-8">{h}</head><body>{b}{foot}</body></html>'
def hl(t,nw=False): return f'<span class="hl"' + (' style="white-space:nowrap"' if nw else '') + f'>{t}</span>'
C1=("C1_internet-segura","2027-02-09_IG-FB",[
 ("fullimg","teal",dict(h1=f'Día de Internet Segura: {hl("4 señales",True)} de que tu web no lo es.',img="lock_teal.jpg",hs=76,ptop=432,ix=150,iy=490,iw=780,p="Desliza y revisa la tuya.")),
 ("item","off",dict(num="01",icon="unlock",h1="Sin candado (HTTPS)",p="Si el navegador avisa de que tu web «no es segura», tus clientes se van antes de leerte.",chip="Solución: certificado SSL")),
 ("item","teal",dict(num="02",icon="refresh",h1="Sin actualizar",p="Plugins y versiones antiguas son la puerta de entrada más habitual para los ataques.",chip="Solución: actualizar a menudo")),
 ("item","yel",dict(num="03",icon="db",h1="Sin copias de seguridad",p="Si algo falla o te hackean, ¿en cuánto tiempo vuelves a estar online?",chip="Solución: copias automáticas")),
 ("item","off",dict(num="04",icon="key",h1="Accesos compartidos",p="Una sola clave para todo y para todos. Cada persona necesita su propio acceso.",chip="Solución: un acceso por persona")),
 ("cover","coral",dict(h1="¿Cuántas de estas 4 señales tiene tu web?",img="lock_yellow.jpg",cardbg="#FFDF78",ctop=345,ch=690,ptop=1068,p="Si no lo sabes, es buen momento para revisarlo.")),
])
C2=("C2_marca-no-es-logo","2027-02-23_IG-FB",[
 ("bleed","teal",dict(h1='Tu marca no es <span class="hl" style="background:#5EBFB5;color:#0B2B3E;white-space:nowrap">un logo.</span>',img="desk1_full.jpg",pos="68%",p="Un logo es solo el principio. Desliza →")),
 ("item","coral",dict(num="01",icon="drop",h1="Color",p="Una paleta corta y coherente: reconocible en un segundo y en cualquier pantalla.",chip="Paleta de 3 a 5 colores")),
 ("item","yel",dict(num="02",icon="type",h1="Tipografía",p="Dos fuentes como mucho. Legibles en el móvil y con carácter propio.",chip="Máximo 2 fuentes")),
 ("item","off",dict(num="03",icon="chat",h1="Tono de voz",p="Hablar igual en la web, en redes y en el WhatsApp. Eso es coherencia.",chip="Una guía de estilo clara")),
 ("item","teal",dict(num="04",icon="layout",h1="Experiencia",p="Tu web, tus redes y tus mensajes se sienten de la misma marca.",chip="Misma imagen en todos los canales")),
 ("recap","yel",dict(h1="¿Se reconocería tu marca sin el logo?",icons=[("drop","Color"),("type","Tipografía"),("chat","Tono"),("layout","Experiencia")],p="Si dudas, empieza por definir tu identidad.")),
])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1350})
        for name,date,sl in (C1,C2):
            n=len(sl)
            for i,(k,bgk,d) in enumerate(sl,1):
                open("tmp.html","w").write(page(k,bgk,i,n,d))
                await pg.goto("file://"+os.getcwd()+"/tmp.html"); await pg.wait_for_timeout(250)
                await pg.screenshot(path=f"{date}_{name}_{i:02d}.png")
        await b.close()
asyncio.run(main())
