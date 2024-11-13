import asyncio
import aiohttp
import time
import os
from bs4 import BeautifulSoup as bs

async def image_dl(session, url, dirname):
    async with session.get(url, ssl = False) as response:
        content = await response.read()
        nombre_img = url.split('/')[-1]
        print(f'{dirname}/{nombre_img}')

        await asyncio.sleep(2)
        with open(f'{dirname}/{nombre_img}', 'wb') as f:
            f.write(content)

async def hilos(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = bs(html, 'html.parser')
        hilo_id = url.split('/')[-1].split('.')[0]
        
        hilo_titulo = soup.find_all(class_="filetitle")

        if len(hilo_titulo) < 1:
            hilo_titulo = ''
        else:
            hilo_titulo = hilo_titulo[0].text.replace('\n', '')

        enlaces_fotos = [span.find('a')['href'] for span in soup.find_all('span', class_='filesize')]

    
        dirname = hilo_id + '.'  + hilo_titulo
        dirname = os.path.join('imgs', dirname)
        os.makedirs(dirname, exist_ok=True)

        tasks = [image_dl(session, enlace, dirname) for enlace in enlaces_fotos]
        await asyncio.gather(*tasks)


async def catalogos(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = bs(html, 'html.parser')
        enlaces_hilos = soup.find_all('a', id='botonresp')

        tasks = [hilos(session, hilo['href']) for hilo in enlaces_hilos]
        await asyncio.gather(*tasks)

async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://www.hispasexy.org/cl'] + [f'https://www.hispasexy.org/cl/{i}.html' for i in range(1, 8)]

        tasks = [catalogos(session, url) for url in urls]
        await asyncio.gather(*tasks)

start = time.perf_counter()       
asyncio.run(main())   
end = time.perf_counter()
print(f'El programa tardo {end-start} segundos')


         
