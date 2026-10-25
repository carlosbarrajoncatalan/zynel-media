import asyncio, sys
from playwright.async_api import async_playwright
NAVY="#0B2B3E"; CORAL="#F26363"; TEAL="#5EBFB5"; YEL="#F2A71B"; OFF="#F2EBEC"
T="""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:SG;src:url(sg.ttf);font-weight:300 700}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:%(bg)s;font-family:SG,sans-serif;color:%(fg)s;position:relative;overflow:hidden}
h1{position:absolute;left:84px;top:%(h1top)spx;width:930px;font-size:%(h1size)spx;line-height:1.3;font-weight:700;letter-spacing:-.01em}
h1 span.hl{background:%(hlbg)s;color:%(hlfg)s;padding:.04em .2em .1em;border-radius:14px;-webkit-box-decoration-break:clone;box-decoration-break:clone;display:inline}
.card{position:absolute;left:84px;top:%(ctop)spx;width:912px;height:%(ch)spx;border-radius:38px;overflow:hidden;background:%(cardbg)s}
.card img{width:100%%;height:100%%;object-fit:%(fit)s;object-position:center}
.body{position:absolute;left:84px;top:%(btop)spx;width:900px;font-size:35px;line-height:1.5;font-weight:400}
.body b{font-weight:700}
.foot{position:absolute;left:84px;bottom:56px;display:flex;align-items:center;gap:22px}
.foot img{width:68px;height:68px}
.foot span{font-size:22px;font-weight:700;letter-spacing:.17em;color:%(footc)s}
</style></head><body>

<h1>%(h1)s</h1>
<div class="card"><img src="%(img)s"></div>
<div class="body">%(body)s</div>
<div class="foot"><img src="%(logo)s"><span>RRSS | WEB | MARKETING | IA</span></div>
</body></html>"""
P={
"pp1":dict(bg=CORAL,fg=NAVY,h1top=112,h1size=80,h1='No seas el <span class="hl">pop-up</span> que todos cierran.',
  hlbg=NAVY,hlfg=OFF,ctop=372,ch=608,cardbg="#fff",fit="contain",img="popups.jpg",
  btop=1016,body="Si tu anuncio interrumpe sin aportar, se cierra.<br>Mensaje claro y oferta concreta.",logo="sq_coral.png",footc="rgba(11,43,62,.72)"),
"sb":dict(bg=YEL,fg=NAVY,h1top=112,h1size=72,h1='Un anuncio dura 30 segundos. <span class="hl">Vender se decide después.</span>',
  hlbg=NAVY,hlfg=OFF,ctop=440,ch=540,cardbg="#E8909A",fit="cover",img="man.jpg",
  btop=1010,body="La atención no es una venta. Entre el anuncio y el cliente hay una web que carga, un formulario y una respuesta rápida.",logo="sq_yellow.png",footc="rgba(11,43,62,.72)"),
"li30":dict(bg=TEAL,fg=NAVY,h1top=112,h1size=72,h1='Así empieza una relación con Zynel:<br><span class="hl">los primeros 30 días.</span>',
  hlbg=NAVY,hlfg=OFF,ctop=444,ch=556,cardbg="#F5F6F1",fit="cover",img="hands.jpg",
  btop=1038,body="Auditoría, estrategia, lanzamiento y datos: así arrancamos con cada cliente.",logo="sq_teal.png",footc="rgba(11,43,62,.72)"),
}
async def main(names):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1350})
        for n in names:
            open(f"{n}.html","w").write(T%P[n])
            await pg.goto(f"file://{__import__('os').getcwd()}/{n}.html"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f"{n}.png"); print(n)
        await b.close()
asyncio.run(main(sys.argv[1:] or list(P)))
