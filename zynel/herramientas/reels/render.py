import sys,subprocess,time
from playwright.sync_api import sync_playwright
name,dur=sys.argv[1],float(sys.argv[2]); only=[float(x) for x in sys.argv[3:]]
fps=30; K=1.0
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto(f'file://{__import__("os").getcwd()}/{name}.html'); pg.wait_for_function('window.ready===true'); pg.evaluate('document.fonts.ready'); time.sleep(.5)
    if only:
        for t in only:
            pg.evaluate('async t=>{seek(t);await window.settle()}',t); pg.screenshot(path=f'prev_{name}_{t}.png')
        sys.exit()
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',f'{name}_v.mp4'],stdin=subprocess.PIPE)
    n=int(dur*K*fps)
    for i in range(n):
        pg.evaluate('async t=>{seek(t);await window.settle()}',i/fps/K); ff.stdin.write(pg.screenshot(type='jpeg',quality=94))
    ff.stdin.close(); ff.wait()
