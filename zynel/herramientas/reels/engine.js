// Motor de reels: todo en función del tiempo t (seek) para renderizar frame a frame.
const NAVY='#0B2B3E', SLATE='#3C4C59', TEAL='#5EBFB5', YEL='#F2A71B', CORAL='#F26363', OFF='#F2EBEC';
const stage=document.getElementById('stage');
const anims=[], vis=[], hooks=[], scenes=[];
const EASE='cubic-bezier(.16,1,.3,1)';
function mk(parent,cls,html,style){const d=document.createElement('div');if(cls)d.className=cls;if(html!=null)d.innerHTML=html;if(style)Object.assign(d.style,style);(parent||stage).appendChild(d);return d;}
function A(n,t0,dur,kf,easing){const a=n.animate(kf,{delay:t0*1000,duration:dur*1000,fill:'both',easing:easing||EASE});a.pause();anims.push(a);return a;}
function show(n,t0,t1){n.style.display='none';vis.push({n,t0,t1});}
function scene(t0,t1,bg){const s=mk(stage,'scene',null,{background:bg||NAVY});s.dataset.t0=t0;s.dataset.t1=t1;scenes.push({s,t0,t1});return s;}
// entrada tipo pop / slide
function pop(n,t0,dy){A(n,t0,.7,[{opacity:0,transform:`translateY(${Math.min(dy??60,26)}px)`},{opacity:1,transform:'translateY(0)'}],'cubic-bezier(.25,.1,.25,1)');}
function kb(n,t0,t1,from,to){A(n,t0,t1-t0,[{transform:from},{transform:to}],'cubic-bezier(.35,0,.25,1)');}
function count(n,t0,t1,a,b,fmt){hooks.push(t=>{let p=Math.min(1,Math.max(0,(t-t0)/(t1-t0)));p=1-Math.pow(1-p,3);n.textContent=fmt(a+(b-a)*p);});}
const fmtEur=v=>Math.round(v).toLocaleString('es-ES')+' €';
const fmtInt=v=>Math.round(v).toLocaleString('es-ES');
function phrase(parent,t0,t1,html,style){const n=mk(parent,'ph',html,style);show(n,t0,t1);pop(n,t0,50);return n;}
function photo(parent,src,style){const i=document.createElement('img');i.src=src;i.className='photo';if(style)Object.assign(i.style,style);parent.appendChild(i);return i;}
const vids=[];
function vid(parent,t0,src0,fps,dir,n){const i=document.createElement('img');Object.assign(i.style,{position:'absolute',left:0,top:0,width:'1080px',height:'1920px'});parent.appendChild(i);vids.push({i,t0,src0,fps,dir:dir||'v/f/',n:n||290});return i;}
window.settle=()=>Promise.all(vids.map(v=>v.i.decode().catch(()=>{})));
function seek(t){
  vids.forEach(v=>{let k=Math.floor((Math.max(t,v.t0)-v.t0)*v.fps+v.src0*v.fps)+1;k=Math.min(k,v.n);v.i.src=v.dir+String(k).padStart(4,'0')+'.jpg';});
  scenes.forEach(o=>{const on=t>=o.t0&&t<o.t1+.35;o.s.style.display=on?'block':'none';o.s.style.opacity=o.t0==0?1:Math.min(1,Math.max(0,(t-o.t0)/.35));});
  vis.forEach(o=>{o.n.style.display=(t>=o.t0&&t<o.t1)?'block':'none';});
  anims.forEach(a=>{a.currentTime=t*1000;});
  hooks.forEach(h=>h(t));
}
function endCard(t0,t1,bg,tile){
  const s=scene(t0,t1,bg);
  const lg=mk(s,'endlogo');
  const b=mk(lg,'',null,{width:'330px',height:'330px',borderRadius:'58px',background:tile||YEL,margin:'0 auto',position:'relative'});
  const zi=document.createElement('img');zi.src='a/z_navy.png';const zw=234,zh=Math.round(234*(zi.naturalHeight||361)/(zi.naturalWidth||373));Object.assign(zi.style,{position:'absolute',left:'48px',top:'51px',width:'234px',height:'227px'});b.appendChild(zi);
  A(lg,t0+.2,.8,[{opacity:0},{opacity:1}],'ease');
  const c=mk(s,'endcta','HABLEMOS<br>EN <span class="hl">ZYNEL</span>');
  A(c,t0+.5,.8,[{opacity:0,transform:'translateY(24px)'},{opacity:1,transform:'translateY(0)'}],'ease');
  const tg=mk(s,'endtag','RRSS &nbsp;|&nbsp; WEB &nbsp;|&nbsp; MARKETING &nbsp;|&nbsp; IA');
  A(tg,t0+1,.8,[{opacity:0},{opacity:1}],'ease');
  return s;
}
