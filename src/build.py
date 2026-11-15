import base64
import time,json
BID=time.strftime('%Y%m%d%H%M%S')
src=open('src.html',encoding='utf-8').read().replace('__BUILD__',BID)
open('version.json','w').write(json.dumps({'v':BID}))
b=base64.b64encode(open('breccia.jpg','rb').read()).decode()
src=src.replace('__BRECCIA__',b)
cdn='''<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/utils/BufferGeometryUtils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/objects/Reflector.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>'''
open('remontti-cad.html','w',encoding='utf-8').write(src.replace('<!--LIBS-->',cdn))
P='lib/package/'
libs=''.join('<script>\n'+open(P+f,encoding='utf-8').read().replace('</script','<\\/script')+'\n</script>\n' for f in ['build/three.min.js','examples/js/controls/OrbitControls.js','examples/js/utils/BufferGeometryUtils.js','examples/js/objects/Reflector.js'])
libs+='<script>\n'+open('lib/jspdf/jspdf.umd.min.js',encoding='utf-8').read().replace('</script','<\\/script')+'\n</script>\n'
local=src.replace('<!--LIBS-->',libs)
# paikallinen tiedosto tarvitsee oman html-rungon
local='<!doctype html>\n<html lang="fi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<style>[hidden]{display:none!important}html,body{margin:0}</style>\n'+local.replace('<div class="app">','</head><body>\n<div class="app">',1)+'\n</body></html>\n'
open('Mallus-Design-Tool.html','w',encoding='utf-8').write(local)
