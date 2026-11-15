import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':1600,'height':920},accept_downloads=True);errs=[]
    pg.on('pageerror',lambda e: errs.append('PAGEERR '+str(e)[:300]));pg.on('console',lambda m: m.type=='error' and 'ERR_TUNNEL' not in m.text and errs.append('CONSOLE '+m.text[:300]))
    pg.goto('file:///home/claude/cad/Mallus-Design-Tool.html');pg.wait_for_timeout(3500)
    step=lambda n: print(n, len(errs), errs[-1] if errs else '')
    r=pg.evaluate("""async()=>{const out=[];const f=S.objects.find(o=>o.type==='floor');let i=0;
      for(const c of LIB)for(const it of c.items){if(it.tool)continue;try{select(null);libAdd(it,c.cat,toWorld(f,0.5+(i%5)*0.5,0.5+Math.floor(i/5)%8*0.5));i++}catch(e){out.push(c.sub+'/'+it.l+': '+e.message)}}
      await new Promise(r=>setTimeout(r,500));return [i,out]}""");step('lib add '+str(r))
    r=pg.evaluate("""async()=>{const out=[];for(const o of S.objects.slice()){try{select(o.id);for(const t of ['props','mats','chk','qty','proj','obj']){try{setTab(t)}catch(e){out.push(t+':'+o.type+':'+e.message)}}const tree=partTree(o);const walk=n=>{for(const x of n){try{selectPart(o.id,x.id);renderProps()}catch(e){out.push('part '+o.type+' '+x.id+': '+e.message)}if(x.children)walk(x.children)}};walk(tree||[])}catch(e){out.push(o.type+' '+o.name+': '+e.message)}}await new Promise(r=>setTimeout(r,500));return out.slice(0,15)}""");step('select all '+str(r))
    for cb in ['hidePrice','hideQty','showDims','showMep','onlyRoom','hideWalls','autoFocus','noBelow','outdoorChk','showClear','blockFurn','followChk']:
        pg.click('#'+cb);pg.wait_for_timeout(150);pg.click('#'+cb);pg.wait_for_timeout(150)
    step('checkboxes')
    pg.evaluate("()=>{openCabs=true;rebuild3D();openCabs=false;rebuild3D()}");step('open cabs')
    pg.evaluate("()=>{for(let k=0;k<25;k++)undo();for(let k=0;k<25;k++)redo()}");pg.wait_for_timeout(500);step('undo/redo')
    pg.evaluate("()=>{addFloor('up','huoneet','2. kerros',2.7,2.4);const f=S.objects.find(o=>o.type==='floor');addObject('stair',{shape:'U'},'Rakenteet','U',toWorld(f,1,1));switchFloor(S.floors[0].id);switchFloor(S.floors[1].id);S.settings.floorView='kaikki';rebuild3D()}");pg.wait_for_timeout(800);step('floors')
    pg.evaluate("()=>{walkStart()}");pg.keyboard.down('w');pg.wait_for_timeout(800);pg.keyboard.up('w');pg.keyboard.press('Escape');step('walk')
    pg.evaluate("async()=>{const t=await exportJSON();importText(t)}");pg.wait_for_timeout(1500);step('json roundtrip '+pg.evaluate("()=>S.floors.length+' floors, '+S.objects.length+' objs'"))
    pg.evaluate("()=>{const t=buildDXF();importDXF(t,'x.dxf')}");step('dxf')
    pg.evaluate("()=>{const L=lightCfg();L.on=true;L.lamps=true;L.hour=20;applyLight();computeQty();cutList()}");step('light/qty/cut')
    pg.evaluate("()=>{photoDialog();setTimeout(()=>{photoStop();photoStart(320,200,4)},100)}");pg.wait_for_function("()=>photo&&photo.done",timeout=300000);pg.click('#dlgOk');step('photo')
    pg.click('#fPdf');pg.wait_for_timeout(300)
    for k in ['plan','dims','clear','view3d','view4','sunSeq','elev','cabDims','mepElev','mepPlan','cut','qty','prices','photo']: pg.check(f'[data-po="{k}"]',timeout=120000)
    import time as _t;_t0=_t.time()
    with pg.expect_download(timeout=300000) as d: pg.click('#dlgOk',timeout=300000)
    print('pdf secs',round(_t.time()-_t0))
    d.value.save_as('/home/claude/cad/smoke.pdf');step('pdf all')
    for h in ['alku','2d','3d','valo','kirjasto','kerrokset','mep','tallennus','pdf','nappain']: pg.evaluate(f"()=>openHelp('{h}')")
    step('help')
    print('\n'.join(errs[:40]))
    b.close()
