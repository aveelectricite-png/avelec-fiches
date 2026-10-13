"""Rend une fiche Facebook Ave'Lec (1080x1350) a partir d'un JSON.
Usage : python3 outil/render.py sujet.json sortie.png
Produit aussi une version PNG palettisee (<1 Mo) adaptee a Facebook."""
import sys, json, asyncio, os
from playwright.async_api import async_playwright
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
async def main():
    data = json.load(open(sys.argv[1], encoding='utf-8'))
    html = TEMPLATE.replace('__DATA__', json.dumps(data, ensure_ascii=False))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1080,'height':1350}, device_scale_factor=1)
        await pg.set_content(html, wait_until='load')
        await pg.screenshot(path=sys.argv[2], full_page=False)
        await b.close()
    im = Image.open(sys.argv[2]).convert('RGB').quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    im.save(sys.argv[2], optimize=True)
asyncio.run(main())
